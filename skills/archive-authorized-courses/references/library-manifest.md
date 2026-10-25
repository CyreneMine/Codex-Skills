# 运行环境与公开资料清单

优先使用当前机器/应用提供的 Python、FFmpeg、ffprobe。AES-128 另需 `cryptography`；缺依赖先说明，不自动运行新下载的安装程序。中文保持 UTF-8。

认证头、签名清单和缓存置于私有任务目录；公开目录仅存课程内容、离线索引和不含认证信息的清单。

## HLS 助手

查看 `python scripts/archive_hls.py --help`。

- `--resource-id` 是已验证配置中的稳定身份，不用签名 URL 代替。
- `--quality` 是主清单 NAME 或 `best`。缓存身份同时核对资源、清晰度、分片路径、时长和 IV。
- `--cache-dir` 是该课独占目录；活动锁、源指纹不符、缓存哈希错误时停止，不覆盖。
- `--headers-file` 是来源到请求头字典，仅向精确匹配来源发送；重定向重新选头。
- `--key-format` 为 `standard` / `qiqiuyun`，后者需要当前 `--key-version`。
- `--expected-streams` 默认 `video,audio`，仅按实际源情况改为 `video`。
- 成功后视频旁生成 `.archive.json`，记录资源、清晰度、时长、流、大小、SHA-256，不含签名 URL 或密钥。
- 已有输出仅在匹配的成功记录与哈希成立时跳过；否则停止，让代理核对，不能直接覆盖或重复下载。

## 索引输入

`library_tools.py` 接受 UTF-8 JSON；所有路径相对资料库根目录，不允许上级路径、绝对路径或符号链接逃逸。

```json
{
  "title": "课程离线资料",
  "items": [
    {"id": "lesson-001", "kind": "video", "title": "第一课", "path": "视频/01 第一课.mp4", "duration_seconds": 480.0},
    {"id": "note-001", "kind": "text", "title": "补充说明", "path": "文字课时/补充说明.html"},
    {"id": "material-001", "kind": "attachment", "title": "源码", "path": "资料/第一课/Example.cs"}
  ],
  "online_only": [{"title": "在线作业", "url": "https://school.example.invalid/task"}]
}
```

实际清单可加 `bytes`、`sha256`，只能填真实文件值。ID、路径不能重复，视频时长须为有限正数。

```powershell
python scripts/library_tools.py audit --root /course-output --manifest /private-work/library.json
python scripts/library_tools.py index --root /course-output --manifest /private-work/library.json
```

`audit` 核对文件、可选大小/哈希、视频时长声明、HTML 本地引用及 `.part` 残留；引用先 URL 解码。它不宣称逐帧解码。

`index` 把清单嵌入 HTML，不通过 `fetch()` 加载本地 JSON；媒体和资料使用相对链接，不依赖外部 CDN。整目录搬移后保留相对结构；`online_only` 显示为需要网络的入口。

## 验证与搬移边界

结构、元数据、完整解码和实际播放是不同证据。合成测试不证明真实站点当前兼容；保存哈希不等于已与官方校验值比较。

跨盘移动先核对明确源/目标、不覆盖冲突；复制后逐文件 SHA-256 相同，再删除再次核对过的原目录。无移动请求不删原件。

工具明确拒绝 `file://` 时，不换通道绕过。交付文件并注明直接本地协议未被工具验证，不能把既有合法 HTTP 播放说成 `file://` 测试。
