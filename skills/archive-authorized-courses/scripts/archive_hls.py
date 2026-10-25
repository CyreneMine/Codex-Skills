"""Archive one already-authorized, finite MPEG-TS HLS lesson. No login/access discovery."""
import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from hls_key_format import normalize_key


def origin(url):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Only ordinary HTTP(S) media URLs without embedded credentials are supported')
    port = parsed.port
    authority = '[' + parsed.hostname + ']' if ':' in parsed.hostname else parsed.hostname
    if port and port != (443 if parsed.scheme == 'https' else 80):
        authority += ':' + str(port)
    return parsed.scheme + '://' + authority


class ScopedHTTP:
    def __init__(self, headers=None, timeout=35):
        self.headers = {}
        for key, value in (headers or {}).items():
            if origin(key) != key.rstrip('/') or not isinstance(value, dict):
                raise ValueError('Request headers must be dictionaries keyed by exact HTTP(S) origins')
            if any('\n' in str(v) or '\r' in str(v) for v in value.values()):
                raise ValueError('Invalid request header value')
            self.headers[origin(key)] = value
        self.timeout = timeout
        owner = self

        class Redirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, request, fp, code, message, response_headers, new_url):
                if urllib.parse.urlsplit(request.full_url).scheme == 'https' and urllib.parse.urlsplit(new_url).scheme != 'https':
                    raise ValueError('HTTPS downgrade redirect refused')
                redirected = super().redirect_request(request, fp, code, message, response_headers, new_url)
                if redirected:
                    for name in list(redirected.headers):
                        redirected.remove_header(name)
                    for name, value in owner.for_url(new_url).items():
                        redirected.add_header(name, value)
                return redirected

        self.opener = urllib.request.build_opener(Redirect())

    def for_url(self, url):
        return {'User-Agent': 'AuthorizedCourseArchive/1.0', **self.headers.get(origin(url), {})}

    def read(self, url):
        request = urllib.request.Request(url, headers=self.for_url(url))
        with self.opener.open(request, timeout=self.timeout) as response:
            return response.read(), response.geturl()


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as file:
        for block in iter(lambda: file.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def write_json(path, value):
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(path)


def attributes(line):
    return {match[0]: match[1] if match[1] else match[2] for match in re.findall(r'([A-Z0-9-]+)=(?:"([^"]*)"|([^,]*))', line.split(':', 1)[1])}


def read_media(playlist, base_url, quality, http, depth=0):
    if depth > 3:
        raise ValueError('Too many nested master playlists')
    if urllib.parse.urlsplit(playlist).scheme in ('http', 'https'):
        raw, base_url = http.read(playlist)
    else:
        raw = Path(playlist).read_bytes()
    text = raw.decode('utf-8-sig')
    if not text.startswith('#EXTM3U'):
        raise ValueError('Response is not an HLS playlist')
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    variants = []
    for index, line in enumerate(lines):
        if line.startswith('#EXT-X-STREAM-INF:'):
            if index + 1 == len(lines) or lines[index + 1].startswith('#'):
                raise ValueError('Master playlist has no variant URI')
            variants.append((attributes(line), lines[index + 1]))
    if variants:
        if not base_url:
            raise ValueError('A local master playlist requires --base-url')
        if quality == 'best':
            chosen = max(variants, key=lambda value: int(value[0].get('BANDWIDTH', '0')))
        else:
            matches = [value for value in variants if value[0].get('NAME') == quality]
            if len(matches) != 1:
                raise ValueError('Requested variant NAME is missing or ambiguous')
            chosen = matches[0]
        return read_media(urllib.parse.urljoin(base_url, chosen[1]), None, quality, http, depth + 1)
    if '#EXT-X-ENDLIST' not in lines:
        raise ValueError('A complete recorded playlist with ENDLIST is required')
    if any(line.startswith(('#EXT-X-MAP:', '#EXT-X-BYTERANGE:')) for line in lines):
        raise ValueError('fMP4 or byte-range HLS requires another compatible authorized downloader')
    sequence = 0
    key_uri = iv = None
    segment_duration = None
    segments = []
    for line in lines:
        if line.startswith('#EXT-X-MEDIA-SEQUENCE:'):
            sequence = int(line.split(':', 1)[1])
        elif line.startswith('#EXT-X-KEY:'):
            fields = attributes(line)
            if fields.get('METHOD') == 'NONE':
                key_uri = iv = None
            elif fields.get('METHOD') == 'AES-128' and fields.get('KEYFORMAT', 'identity') == 'identity':
                key_uri = urllib.parse.urljoin(base_url or '', fields['URI'])
                origin(key_uri)
                iv = bytes.fromhex(fields['IV'][2:]) if 'IV' in fields else None
                if iv is not None and len(iv) != 16:
                    raise ValueError('Invalid AES IV length')
            else:
                raise ValueError('Unsupported key method/format; no DRM or authorization bypass is implemented')
        elif line.startswith('#EXTINF:'):
            segment_duration = float(line.split(':', 1)[1].split(',', 1)[0])
            if not math.isfinite(segment_duration) or segment_duration <= 0:
                raise ValueError('Invalid segment duration')
        elif not line.startswith('#'):
            uri = urllib.parse.urljoin(base_url or '', line)
            origin(uri)
            if segment_duration is None:
                raise ValueError('Segment has no EXTINF')
            actual_iv = iv if iv is not None else (sequence + len(segments)).to_bytes(16, 'big')
            segments.append({'url': uri, 'key': key_uri, 'iv': actual_iv, 'duration': segment_duration})
            segment_duration = None
    if not segments:
        raise ValueError('Playlist contains no segments')
    return segments


def transport_stream(data):
    return len(data) >= 376 and len(data) % 188 == 0 and data[0] == 0x47 and data[188] == 0x47


def probe(path, executable, expected_streams):
    process = subprocess.run([executable, '-v', 'error', '-show_entries', 'format=duration,size:stream=codec_type,codec_name,width,height', '-of', 'json', str(path)], capture_output=True, encoding='utf-8', check=True)
    result = json.loads(process.stdout)
    if not set(expected_streams) <= {stream['codec_type'] for stream in result['streams']}:
        raise ValueError('Expected audio/video streams are missing')
    duration = float(result['format']['duration'])
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError('Output duration is invalid')
    return result


def archive(args, emit=print):
    output = Path(args.output).resolve()
    if not args.resource_id.strip() or output.suffix.lower() != '.mp4':
        raise ValueError('A nonempty stable resource ID and .mp4 output are required')
    report_path = output.with_name(output.name + '.archive.json')
    if output.exists():
        if report_path.exists():
            report = json.loads(report_path.read_text(encoding='utf-8'))
            if report.get('resource_id') == args.resource_id and report.get('quality') == args.quality and sha256_file(output) == report.get('sha256'):
                emit(json.dumps({'status': 'already_verified', 'bytes': output.stat().st_size}))
                return report
        raise FileExistsError('Existing output has no matching verified record; no download was started')
    partial = output.with_name(output.stem + '.part.mp4')
    if partial.exists():
        raise FileExistsError('Existing partial output must be reviewed before continuing')
    cache = Path(args.cache_dir).resolve()
    cache.mkdir(parents=True, exist_ok=True)
    lock = cache / '.active.lock'
    with lock.open('x', encoding='utf-8') as file:
        file.write(str(os.getpid()))
    try:
        headers = json.loads(Path(args.headers_file).read_text(encoding='utf-8-sig')) if args.headers_file else {}
        http = ScopedHTTP(headers, args.timeout)
        segments = read_media(args.playlist, args.base_url, args.quality, http)
        descriptor = {'resource_id': args.resource_id, 'quality': args.quality, 'segments': [{'path': urllib.parse.urlunsplit(urllib.parse.urlsplit(s['url'])._replace(query='', fragment='')), 'duration': s['duration'], 'iv': s['iv'].hex(), 'encrypted': bool(s['key'])} for s in segments]}
        fingerprint = hashlib.sha256(json.dumps(descriptor, sort_keys=True).encode('utf-8')).hexdigest()
        state_path = cache / 'state.json'
        state = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {'fingerprint': fingerprint, 'segments': {}}
        if state['fingerprint'] != fingerprint:
            raise ValueError('Cache source/quality/segments changed; no cached files were overwritten')
        write_json(state_path, state)
        key_cache = {}
        merged = cache / 'assembled.ts'
        with merged.open('wb') as destination:
            for number, segment in enumerate(segments):
                path = cache / f'{number:06d}.ts'
                previous = state['segments'].get(str(number))
                if path.exists():
                    if previous is None or sha256_file(path) != previous['sha256']:
                        raise ValueError('Cached segment hash mismatch; cached files left unchanged')
                    clear = path.read_bytes()
                else:
                    if segment['key'] and segment['key'] not in key_cache:
                        response, _ = http.read(segment['key'])
                        key_cache[segment['key']] = normalize_key(response, args.key_format, args.key_version)
                    encrypted, _ = http.read(segment['url'])
                    clear = encrypted
                    if segment['key']:
                        from cryptography.hazmat.primitives import padding
                        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
                        decryptor = Cipher(algorithms.AES(key_cache[segment['key']]), modes.CBC(segment['iv'])).decryptor()
                        padded = decryptor.update(encrypted) + decryptor.finalize()
                        unpadder = padding.PKCS7(128).unpadder()
                        clear = unpadder.update(padded) + unpadder.finalize()
                    if not transport_stream(clear):
                        raise ValueError('Decrypted segment is not valid MPEG-TS')
                    temporary = path.with_suffix('.partial')
                    with temporary.open('xb') as file:
                        file.write(clear)
                    temporary.rename(path)
                    state['segments'][str(number)] = {'sha256': hashlib.sha256(clear).hexdigest(), 'bytes': len(clear)}
                    write_json(state_path, state)
                destination.write(clear)
                if number % 10 == 0 or number + 1 == len(segments):
                    emit(json.dumps({'stage': 'segments', 'complete': number + 1, 'total': len(segments)}))
        output.parent.mkdir(parents=True, exist_ok=True)
        with (cache / 'remux.log').open('w', encoding='utf-8') as log:
            process = subprocess.run([args.ffmpeg, '-nostdin', '-n', '-hide_banner', '-loglevel', 'error', '-i', str(merged), '-c', 'copy', '-movflags', '+faststart', str(partial)], stdout=log, stderr=log)
        if process.returncode:
            raise RuntimeError('Local remux failed; inspect private cache/remux.log')
        info = probe(partial, args.ffprobe, args.expected_streams.split(','))
        expected = sum(segment['duration'] for segment in segments)
        if abs(float(info['format']['duration']) - expected) > 2:
            raise ValueError('Output duration differs from complete playlist')
        digest = sha256_file(partial)
        # Exclusive creation works without depending on platform-specific rename overwrite rules.
        created = False
        try:
            with output.open('xb') as destination, partial.open('rb') as source:
                created = True
                shutil.copyfileobj(source, destination, 1024 * 1024)
            if sha256_file(output) != digest:
                raise ValueError('Final copy hash mismatch')
        except Exception:
            if created:
                output.unlink()
            raise
        report = {'resource_id': args.resource_id, 'quality': args.quality, 'duration_seconds': float(info['format']['duration']), 'bytes': output.stat().st_size, 'sha256': digest, 'streams': info['streams'], 'segments': len(segments)}
        write_json(report_path, report)
        partial.unlink()
        merged.unlink()
        for number in range(len(segments)):
            (cache / f'{number:06d}.ts').unlink()
        emit(json.dumps({'status': 'complete', 'bytes': report['bytes'], 'duration_seconds': report['duration_seconds']}))
        return report
    finally:
        lock.unlink()


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument('--playlist', required=True, help='Current authorized master/media URL or private local playlist')
    result.add_argument('--base-url', help='Original HTTP(S) URL for a saved local playlist')
    result.add_argument('--headers-file', help='Private JSON mapping exact origins to request-header dictionaries')
    result.add_argument('--resource-id', required=True, help='Verified stable resource identity, independent of signing tokens')
    result.add_argument('--quality', default='best', help='Exact variant NAME, or best')
    result.add_argument('--key-format', choices=('standard', 'qiqiuyun'), default='standard')
    result.add_argument('--key-version', type=int)
    result.add_argument('--cache-dir', required=True)
    result.add_argument('--output', required=True)
    result.add_argument('--expected-streams', default='video,audio')
    result.add_argument('--timeout', type=float, default=35)
    result.add_argument('--ffmpeg', default='ffmpeg')
    result.add_argument('--ffprobe', default='ffprobe')
    return result


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    arguments = parser().parse_args()
    try:
        archive(arguments)
    except Exception as error:
        # Do not print urllib URLs, signing queries, request headers, or server response bodies.
        message = re.sub(r'https?://\S+', '[URL]', str(error))
        print(json.dumps({'status': 'failed', 'type': type(error).__name__, 'message': message}, ensure_ascii=False))
        sys.exit(1)
