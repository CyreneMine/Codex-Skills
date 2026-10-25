"""Offline synthetic-media regression tests; never contacts a real course service."""
import collections
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
import unittest
import uuid

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from archive_hls import ScopedHTTP, archive, parser, sha256_file
from hls_key_format import ORDERS_21, UnsupportedKeyFormat, normalize_key
from library_tools import audit, build_index, local_path


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        state = self.server.state
        state['counts'][self.path] += 1
        state['headers'][self.path] = dict(self.headers)
        if self.path == '/redirect':
            self.send_response(302)
            self.send_header('Location', state['redirect'])
            self.end_headers()
            return
        if self.path == '/key' and state['counts']['/key'] > state['key_limit']:
            self.send_error(400)
            return
        if self.path == '/1.ts' and state['fail_second']:
            state['fail_second'] = False
            self.send_error(503)
            return
        if self.path not in state['files']:
            self.send_error(404)
            return
        data = state['files'][self.path]
        self.send_response(200)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


def server():
    instance = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    instance.state = {'files': {}, 'counts': collections.Counter(), 'headers': {}, 'key_limit': 100, 'fail_second': False}
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    return instance, f'http://127.0.0.1:{instance.server_port}'


def encoded_key(key, version, marker=1):
    if version <= 3:
        raw = bytearray(16)
        for index, position in enumerate((8,9,2,3,4,5,6,7,0,1,10,11,12,13,14,15)):
            raw[position] = key[index]
        return b'X' + bytes(raw)
    raw = bytearray(b'x' * 21)
    for index, position in enumerate(ORDERS_21[version][marker]):
        raw[position] = key[index]
    raw[-1] = 48 + marker
    return bytes(raw)


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
            raise RuntimeError('FFmpeg and ffprobe are required for this offline self-test')
        cls.base_directory = Path(os.environ.get('COURSE_ARCHIVE_TEST_DIR', tempfile.gettempdir())).resolve()
        cls.root = cls.base_directory / ('authorized-course-test-' + uuid.uuid4().hex)
        cls.root.mkdir()
        cls.addClassCleanup(cls.cleanup_directory)
        fixture = cls.root / 'fixture'
        fixture.mkdir()
        process = subprocess.run(['ffmpeg', '-nostdin', '-y', '-v', 'error', '-f', 'lavfi', '-i', 'color=c=blue:s=160x90:r=10', '-f', 'lavfi', '-i', 'sine=frequency=330:sample_rate=16000', '-t', '3', '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', '-g', '10', '-sc_threshold', '0', '-c:a', 'aac', '-b:a', '24k', '-f', 'hls', '-hls_time', '1', '-hls_playlist_type', 'vod', '-hls_segment_filename', str(fixture / '%d.ts'), str(fixture / 'original.m3u8')], capture_output=True)
        if process.returncode:
            raise RuntimeError('Synthetic FFmpeg fixture generation failed')
        cls.parts = [path.read_bytes() for path in sorted(fixture.glob('*.ts'))]
        cls.http, cls.base = server()
        cls.sink, cls.sink_base = server()
        cls.key = bytes(range(16))

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown()
        cls.sink.shutdown()
        cls.http.server_close()
        cls.sink.server_close()

    @classmethod
    def cleanup_directory(cls):
        resolved = cls.root.resolve()
        if resolved.parent != cls.base_directory or not resolved.name.startswith('authorized-course-test-'):
            raise RuntimeError('Refusing cleanup outside the isolated test directory')
        if resolved.exists():
            shutil.rmtree(resolved)

    def setUp(self):
        self.http.state.update(files={}, counts=collections.Counter(), headers={}, key_limit=1, fail_second=False)
        self.sink.state.update(files={'/echo':b'ok'}, counts=collections.Counter(), headers={})

    def playlist(self, version=6):
        state = self.http.state
        state['files']['/key'] = encoded_key(self.key, version)
        lines = ['#EXTM3U', '#EXT-X-VERSION:3', '#EXT-X-TARGETDURATION:1', '#EXT-X-MEDIA-SEQUENCE:0']
        for index, clear in enumerate(self.parts):
            iv = (index + 1).to_bytes(16, 'big')
            padder = padding.PKCS7(128).padder()
            padded = padder.update(clear) + padder.finalize()
            encryptor = Cipher(algorithms.AES(self.key), modes.CBC(iv)).encryptor()
            state['files'][f'/{index}.ts'] = encryptor.update(padded) + encryptor.finalize()
            lines += [f'#EXT-X-KEY:METHOD=AES-128,URI="{self.base}/key",IV=0x{iv.hex()}', '#EXTINF:1.000,', f'{self.base}/{index}.ts']
        lines += ['#EXT-X-ENDLIST']
        state['files']['/media.m3u8'] = '\n'.join(lines).encode()
        state['files']['/master.m3u8'] = f'#EXTM3U\n#EXT-X-STREAM-INF:BANDWIDTH=1000,NAME=high\n{self.base}/media.m3u8\n'.encode()

    def arguments(self, name, version=6):
        return parser().parse_args(['--playlist',self.base+'/master.m3u8','--resource-id','synthetic-resource','--quality','high','--key-format','qiqiuyun','--key-version',str(version),'--cache-dir',str(self.root/name/'cache'),'--output',str(self.root/name/'lesson.mp4')])

    def test_key_formats_and_rejections(self):
        for version in range(1, 11):
            for marker in (0, 1, 2):
                self.assertEqual(normalize_key(encoded_key(self.key,version,marker),'qiqiuyun',version),self.key)
        self.assertEqual(normalize_key(self.key),self.key)
        for version in (0,11,99):
            with self.assertRaises(UnsupportedKeyFormat):normalize_key(self.key,'qiqiuyun',version)
        with self.assertRaises(UnsupportedKeyFormat):normalize_key(b'not-a-standard-key')
        # Fixed protocol examples cover both reorder selectors and arithmetic key expansion.
        response=b'a0bcdefghijklmnopqrs'
        expected=(b'a0bcdefgrpomlkjh',b'a0blmnopqrdefgij',b'a0bcdopqrjklmfgh')
        for version,key in enumerate(expected,1):self.assertEqual(normalize_key(response,'qiqiuyun',version),key)
        expansions=((1,b'bbcda2gha4b4mnoc4d4t',b'bbcda2gh!"mno#>t'),(2,b'a2ca4fghb4klmnc4qrd4',b'a2c!fgh"klmn#qr>'),(3,b'a2cdea4hib4lmc4pq d4t'.replace(b' ',b''),b'a2cde!hi"lm#pq>t'))
        for version,response,key in expansions:self.assertEqual(normalize_key(response,'qiqiuyun',version),key)

    def test_end_to_end_one_use_key_and_no_duplicate(self):
        self.playlist()
        args=self.arguments('complete')
        report=archive(args,emit=lambda value:None)
        self.assertEqual(self.http.state['counts']['/key'],1)
        self.assertTrue(Path(args.output).is_file())
        self.assertEqual(report['segments'],len(self.parts))
        self.assertEqual({s['codec_type'] for s in report['streams']},{'audio','video'})
        self.assertAlmostEqual(report['duration_seconds'],3.0,delta=.3)
        before=dict(self.http.state['counts'])
        archive(args,emit=lambda value:None)
        self.assertEqual(dict(self.http.state['counts']),before)

    def test_resume_skips_verified_segment(self):
        self.playlist()
        self.http.state['fail_second']=True
        args=self.arguments('resume')
        with self.assertRaises(Exception):archive(args,emit=lambda value:None)
        self.assertFalse(Path(args.output).exists())
        self.assertEqual(self.http.state['counts']['/0.ts'],1)
        self.http.state['key_limit']=2
        archive(args,emit=lambda value:None)
        self.assertEqual(self.http.state['counts']['/0.ts'],1)
        self.assertEqual(self.http.state['counts']['/key'],2)

    def test_origin_headers_do_not_follow_redirect(self):
        self.http.state['redirect']=self.sink_base+'/echo'
        context=ScopedHTTP({self.base:{'Cookie':'fixture_session=synthetic','Authorization':'Bearer synthetic-fixture'},self.sink_base:{'X-Fixture':'sink'}})
        content,_=context.read(self.base+'/redirect')
        self.assertEqual(content,b'ok')
        self.assertEqual(self.http.state['headers']['/redirect']['Cookie'],'fixture_session=synthetic')
        received=self.sink.state['headers']['/echo']
        self.assertNotIn('Cookie',received)
        self.assertNotIn('Authorization',received)
        self.assertEqual(received['X-Fixture'],'sink')

    def test_changed_source_and_corrupt_cache_stop(self):
        self.playlist()
        self.http.state['fail_second']=True
        args=self.arguments('changed')
        with self.assertRaises(Exception):archive(args,emit=lambda value:None)
        args.resource_id='different-resource'
        with self.assertRaises(ValueError):archive(args,emit=lambda value:None)
        self.assertEqual(self.http.state['counts']['/0.ts'],1)
        args.resource_id='synthetic-resource'
        (Path(args.cache_dir)/'000000.ts').write_bytes(b'corrupted-cache')
        with self.assertRaises(ValueError):archive(args,emit=lambda value:None)
        self.assertFalse(Path(args.output).exists())

    def test_library_paths_images_and_index(self):
        root=self.root/'library'
        (root/'images').mkdir(parents=True,exist_ok=True)
        (root/'images'/'图.png').write_bytes(b'local-image-fixture')
        (root/'note.html').write_text('<p>offline note</p><img src="images/%E5%9B%BE.png">',encoding='utf-8')
        manifest=self.root/'library.json'
        data={'title':'Synthetic offline library','items':[{'id':'note','kind':'text','title':'</script><script>unsafe()</script>','path':'note.html','sha256':sha256_file(root/'note.html')}]}
        manifest.write_text(json.dumps(data),encoding='utf-8')
        self.assertTrue(audit(root,manifest)['ok'])
        index=build_index(root,manifest)
        self.assertNotIn('</script><script>unsafe()',index.read_text(encoding='utf-8'))
        with self.assertRaises(ValueError):local_path(root.resolve(),'../outside')
        with self.assertRaises(ValueError):local_path(root.resolve(),'%2e%2e/outside')
        (root/'note.html').write_text('<img src="https://media.example.invalid/image.png">',encoding='utf-8')
        result=audit(root,manifest)
        self.assertFalse(result['ok'])
        self.assertIn('remote_asset_in_offline_text',{entry['error'] for entry in result['errors']})


if __name__=='__main__':
    unittest.main(verbosity=2)
