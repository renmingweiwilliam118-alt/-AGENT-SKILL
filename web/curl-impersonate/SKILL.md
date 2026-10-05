---
name: curl-impersonate
description: Bypass TLS/HTTP2 fingerprinting by making curl handshakes byte-identical to Chrome/Edge/Firefox/Safari — curl-impersonate (prebuilt binaries target Linux/macOS; knowledge reference for this Windows box). Use when a plain request is blocked by TLS/HTTP2 fingerprint checks that a normal curl/requests/python-requests does not survive. On this Windows machine it's a knowledge aid — the prebuilt .exe are Linux/macOS; for live work prefer Scrapling (impersonate='chrome') which ships a Windows-friendly path.
license: MIT (curl-impersonate)
---

# curl-impersonate

A patched curl that does **TLS + HTTP/2 handshakes identical to a real browser** (Chrome/Edge/Safari via BoringSSL; Firefox via NSS), so sites that gate on TLS/HTTP2 fingerprint can't tell it apart from a browser.

## 概念（对本机的意义）
- 核心原理：普通 HTTP 客户端的 Client Hello / HTTP2 SETTINGS 和浏览器差异极大，服务器据此做 **TLS/HTTP2 指纹识别** 来拦 bot。
- curl-impersonate 把 curl 换成 BoringSSL/NSS 编译 + 改 TLS 扩展 + 改 HTTP2 设置，握手"长得像浏览器"。
- **已核实：它所有 release 都没有 Windows 预构建二进制**（只 Linux/macOS），本机无法直接跑 curl-impersonate.exe。所以本机**当知识用**，实际规避 TLS/HTTP2 指纹用 **Scrapling**（`Fetcher.get(url, impersonate='chrome')`，依赖已装好的 `curl_cffi`，Windows 友好，已验证能抓 200）。

## 等价的本机可用替代
```python
# 用 curl_cffi（Scrapling 已带）模拟 Chrome 指纹 —— 比装 curl-impersonate 更省事
from scrapling.fetchers import Fetcher
page = Fetcher.get("https://example.com", impersonate="chrome")
```

## 什么时候用哪个
| 场景 | 选 |
|---|---|
| 被 TLS/HTTP2 指纹拦、普通请求 403/挑战 | **Scrapling impersonate**（本机） |
| 必须用 C 级 curl-impersonate | 下载对应预构建 + 装 NSS/BoringSSL（主要 Linux/macOS） |

## 坑
- 加某些 curl 旗标会改变 TLS 签名反而被识别，别乱加。
- 预构建要在目标机装 NSS/CA 证书依赖。
