"""Audit a public course-file manifest and build a self-contained relative-link index."""
import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
import math
import re
import sys
import urllib.parse
from pathlib import Path


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as file:
        for block in iter(lambda: file.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def local_path(root, relative):
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise ValueError('Use nonempty slash-separated relative paths')
    parsed = urllib.parse.urlsplit(relative)
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError('Manifest paths must be plain local relative paths')
    decoded = urllib.parse.unquote(parsed.path)
    if Path(decoded).is_absolute() or re.match(r'^[A-Za-z]:', decoded):
        raise ValueError('Absolute manifest path refused')
    result = (root / decoded).resolve()
    if result == root or not result.is_relative_to(root):
        raise ValueError('Manifest path escaped library root')
    return result


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = []

    def handle_starttag(self, tag, attributes):
        for name, value in attributes:
            if value and name in ('src', 'href'):
                self.values.append((tag, name, value))


def load_library(root, manifest):
    root = Path(root).resolve()
    data = json.loads(Path(manifest).read_text(encoding='utf-8-sig'))
    ids, paths = set(), set()
    for item in data['items']:
        if item['kind'] not in ('video', 'text', 'attachment'):
            raise ValueError('Unknown library item kind')
        if not isinstance(item.get('id'), str) or not item['id'] or item['id'] in ids:
            raise ValueError('Duplicate or invalid item ID')
        ids.add(item['id'])
        path = local_path(root, item['path'])
        identity = str(path).casefold()
        if identity in paths:
            raise ValueError('Duplicate library file path')
        paths.add(identity)
        if item['kind'] == 'video':
            duration = float(item['duration_seconds'])
            if not math.isfinite(duration) or duration <= 0:
                raise ValueError('Video duration must be finite and positive')
    return root, data


def audit(root, manifest):
    root, data = load_library(root, manifest)
    errors = []
    for item in data['items']:
        path = local_path(root, item['path'])
        if not path.is_file():
            errors.append({'id': item['id'], 'error': 'missing_file'})
            continue
        if 'bytes' in item and path.stat().st_size != item['bytes']:
            errors.append({'id': item['id'], 'error': 'size_mismatch'})
        if 'sha256' in item and digest(path) != item['sha256']:
            errors.append({'id': item['id'], 'error': 'hash_mismatch'})
        if item['kind'] == 'text' and path.suffix.lower() in ('.html', '.htm'):
            parser = References()
            parser.feed(path.read_text(encoding='utf-8-sig'))
            for tag, attribute, value in parser.values:
                parsed = urllib.parse.urlsplit(value)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    if attribute == 'src' and (parsed.scheme in ('http', 'https') or parsed.netloc):
                        errors.append({'id': item['id'], 'error': 'remote_asset_in_offline_text'})
                    continue
                decoded = urllib.parse.unquote(parsed.path)
                target = (path.parent / decoded).resolve()
                if not target.is_relative_to(root) or not target.is_file():
                    errors.append({'id': item['id'], 'error': 'missing_or_external_local_reference'})
    partials = [str(path.relative_to(root)) for path in root.rglob('*') if path.is_file() and re.search(r'\.part(?:\.|$)|\.partial(?:\.|$)', path.name)]
    return {'items': len(data['items']), 'errors': errors, 'partials': partials, 'ok': not errors and not partials}


def build_index(root, manifest):
    root, data = load_library(root, manifest)
    result = audit(root, manifest)
    if not result['ok']:
        raise ValueError('Library audit failed; incomplete index was not written')
    items = []
    for item in data['items']:
        relative = local_path(root, item['path']).relative_to(root).as_posix()
        items.append({'title': item['title'], 'kind': item['kind'], 'url': urllib.parse.quote(relative, safe='/')})
    encoded = json.dumps(items, ensure_ascii=False).replace('<', '\\u003c')
    online = ''
    for link in data.get('online_only', []):
        parsed = urllib.parse.urlsplit(link['url'])
        if parsed.scheme not in ('http', 'https'):
            raise ValueError('Online-only link must use HTTP(S)')
        online += '<li><a target="_blank" rel="noopener" href="' + html.escape(link['url'], quote=True) + '">' + html.escape(link['title']) + '</a>（需要网络）</li>'
    title = html.escape(data.get('title', '课程离线资料'))
    page = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>__TITLE__</title>
<style>body{max-width:1200px;margin:32px auto;padding:0 20px;font:16px/1.7 system-ui;color:#173245;background:#f5f7fa}h1{font-size:27px}main{display:grid;grid-template-columns:320px 1fr;gap:22px}aside,section{background:white;padding:18px;border-radius:12px}input{box-sizing:border-box;width:100%;padding:10px;font:inherit}button{display:block;width:100%;padding:12px;border:0;background:#f1f6fa;text-align:left;margin:6px 0;cursor:pointer;font:inherit}video{width:100%;background:#111}a{color:#1468ab}#lessons{max-height:560px;overflow:auto}.files li{overflow-wrap:anywhere}@media(max-width:760px){main{display:block}aside{margin-bottom:18px}}</style>
<h1>__TITLE__</h1><main><aside><input id="search" aria-label="搜索视频" placeholder="搜索视频课时"><div id="lessons"></div></aside><section><video id="player" controls preload="metadata"></video><h2 id="current">选择课时播放</h2><a id="standalone" target="_blank" rel="noopener">单独打开本地视频</a></section></main>
<h2>文字与配套资料</h2><ul id="files" class="files"></ul><h2>在线内容</h2><ul>__ONLINE__</ul><p>保留目录内相对位置，双击本页面使用本地文件。</p>
<script id="data" type="application/json">__DATA__</script><script>
const items=JSON.parse(document.getElementById('data').textContent),list=document.getElementById('lessons'),search=document.getElementById('search');
function choose(item,play){document.getElementById('player').src=item.url;document.getElementById('current').textContent=item.title;document.getElementById('standalone').href=item.url;if(play)document.getElementById('player').play().catch(()=>{})}
function render(){list.replaceChildren();for(const item of items.filter(x=>x.kind==='video'&&x.title.toLocaleLowerCase().includes(search.value.toLocaleLowerCase()))){const button=document.createElement('button');button.textContent=item.title;button.onclick=()=>choose(item,true);list.append(button)}}
for(const item of items.filter(x=>x.kind!=='video')){const row=document.createElement('li'),link=document.createElement('a');link.href=item.url;link.textContent=item.title;link.target='_blank';row.append(link);document.getElementById('files').append(row)}search.oninput=render;render();const first=items.find(x=>x.kind==='video');if(first)choose(first,false);
</script></html>'''
    page = page.replace('__TITLE__', title).replace('__ONLINE__', online).replace('__DATA__', encoded)
    destination = root / '离线学习目录.html'
    if destination.is_symlink():
        raise ValueError('Index path is a symlink')
    destination.write_text(page, encoding='utf-8')
    return destination


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('audit', 'index'))
    parser.add_argument('--root', required=True)
    parser.add_argument('--manifest', required=True)
    args = parser.parse_args()
    try:
        if args.action == 'audit':
            result = audit(args.root, args.manifest)
            print(json.dumps(result, ensure_ascii=False))
            sys.exit(0 if result['ok'] else 1)
        else:
            print(json.dumps({'index': str(build_index(args.root, args.manifest))}, ensure_ascii=False))
    except (ValueError, KeyError, OSError) as error:
        print(json.dumps({'status': 'failed', 'type': type(error).__name__}))
        sys.exit(1)
