# EduSoho / 气球云的授权 HLS 适配

来自一次已购、可正常播放课程的归档。以下是观察到的协议，不保证所有 EduSoho 站点兼容，也不提供额外观看权限。

## 配置与授权

1. 在可播放课时确认活动框架。观察到 `#task-content-iframe` 再嵌入跨域播放器，主框架日志可能没有媒体请求。
2. 正常授权活动页面的 `#lesson-video-content` 含当前 `data-token`、`data-file-global-id`。只读取所需字段，放在私有工作目录。
3. 以当前播放器实际调用的请求为模板。该次服务为 `https://play.qiqiuyun.net/sdk_api/play`，参数包括 `resNo`、`token`、`ssl`、`sdkType`、`lang`、`callback`。
4. 每课新读活动页，立即请求初始化配置。已被浏览器使用的参数可能无法重放；HTTP 200 JSONP 也可能只是 `A bad token`。
5. 成功 JSONP 含 `type`、`args`、`appId`、`version`，主清单在 `args.playlist`。检查结构与错误字段，不能只看 HTTP 状态。
6. 从主清单选择实际声明的“超清”等 variant，再读取媒体清单；完整录播需要 `#EXT-X-ENDLIST`。

Cookie 只用于所属课程来源。SDK、CDN 和密钥接口分别使用实际所需头；跨域跳转不能原样转发源站 Cookie。临时链接可能单次使用，避免“先检查一次、再让下载器读取同一链接”。

## 自定义密钥封装

该次清单声明 `METHOD=AES-128`，响应却可为 17、20、21 字节。官方客户端按**本次初始化的 version**还原为 16 字节；版本会随请求变化。

[`../scripts/hls_key_format.py`](../scripts/hls_key_format.py) 支持当次观察到的版本 1–10。它只转换正常会话已提供的响应，不生成服务器授权，不读取浏览器/CDM 内存，不包含厂商播放器源码。未知版本或长度报错。

公开协议核对来源：

- `https://service-cdn-ali.qiqiuyun.net/js-sdk-v2/sdk-v1.js`
- `https://service-cdn-ali.qiqiuyun.net/js-sdk-v2/media-core/hls/1.6.5/index.js`

站点变化时重新核对实际加载的客户端，不盲用旧顺序，不截取“最后 16 字节”。Widevine、FairPlay 等 DRM/CDM 不走此适配路径。

## 助手调用

浏览器/站点适配先完成正常登录、获取新配置及清单。助手不登录、猜课时 ID 或获取权限。

私有请求头 JSON 采用“精确来源 → 请求头”的结构，真实值只在本地填写：

```json
{
  "https://school.example.invalid": {"Cookie": "LOCAL_SESSION_VALUE"},
  "https://media.example.invalid": {
    "User-Agent": "CURRENT_BROWSER_USER_AGENT",
    "Referer": "https://school.example.invalid/"
  }
}
```

来源包含协议、主机和可选端口。跨来源重定向后重新选择请求头；不要把认证文件放入待提交目录。

```powershell
python scripts/archive_hls.py `
  --playlist /private-work/current-media.m3u8 `
  --base-url https://media.example.invalid/current-media.m3u8 `
  --headers-file /private-work/headers.json `
  --resource-id current-file-id --quality 超清 `
  --key-format qiqiuyun --key-version 10 `
  --cache-dir /private-work/lesson-cache `
  --output /course-output/01-introduction.mp4
```

域名、文件 ID 为说明用值；版本必须来自当前配置。`--playlist` 也可为当前清单 URL，主清单只读一次。默认要求视频和音频；已确认无声时传 `--expected-streams video`。

支持完整 MPEG-TS HLS、AES-128 或未加密分片；字节范围、fMP4 初始化段、SAMPLE-AES 等明确报错，改用符合当前授权和工具约束的兼容方式。

## 资料和动态文字

- 根据真实分页链接枚举资料，以课时/资料 ID 区分同名文件；保持原始字节，不执行附件代码。
- 观察到文字页只有 `.text-activity-content` 容器，LTC 的 `getActivity` 才返回正文。
- 父页面 `#ltc-source-list` JSON 的 `context.activityId` 提供 ID，正常映射为只读 `GET /api/activities/:id`。
- 该次需要 `Accept: application/vnd.edusoho.v2+json`，另有 `X-Requested-With` 和当前 CSRF 头；不带正确 API 版本的 404 不等于没有正文。仅按正常客户端要求使用这些头。
- 取得正文后清理脚本/事件，保留文本、代码和图片，再核对离线渲染。
- 在线作业 `content` 为空不能当成空题目，也不授权创建答题记录或读取隐藏答案。
