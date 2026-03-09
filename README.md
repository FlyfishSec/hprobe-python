# Hprobe 🚀 [![PyPI Downloads](https://static.pepy.tech/personalized-badge/hprobe?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://github.com/FlyfishSec/hprobe)

A high-performance HTTP probing tool for asset discovery.

`hprobe` 是一个基于 Rust 实现的 高性能 HTTP 探测引擎，提供直观易用的 Python API。
它支持同步与异步扫描，在大规模目标场景下能够高效完成 HTTP 服务探测、TLS 信息解析以及应用指纹与技术栈识别，适用于资产发现、网络空间测绘与自动化安全评估。

🔗 **GitHub:** [https://github.com/FlyfishSec/hprobe-python](https://github.com/FlyfishSec/hprobe-python)

---

## Core Advantages 📌| 核心优势

1. **Tokio 异步运行时，极致高并发**
   - 基于 Tokio 异步运行时构建，充分利用多核性能，支撑大规模高并发探测

2. **纳秒级 ASN 查询**  
   - 自定义二进制结构体，采用零拷贝设计 + mmap 内存映射 + 二分查找，实现纳秒级 ASN 信息查询

3. **极速 Web 指纹识别**  
   - 集成 17000 + 指纹规则，进程内单例懒加载，10MB HTML 毫秒级指纹识别

## Quick Start⚡| 快速开始

```bash
# PyPI 安装（Python >=3.7）
pip install hprobe
```

```bash
python -c "import hprobe; print(
    hprobe.HprobeScanner()
        .set_target('https://httpbin.org')
        .set_tls_info(True)
        .set_tech_detect(True)
        .set_fingerprint(True)
        .set_asn(True)
        .scan()
)"

[
  {
    "target": "httpbin.org",
    "resolved_ips": [
      "3.210.41.225", "3.223.36.72", "52.204.75.48", "54.236.169.179", "44.197.91.61", "3.95.121.17"
      ],
    "scheme": "https",
    "host": "httpbin.org",
    "url": "https://httpbin.org:443",
    "port": 443,
    "method": "GET",
    "status_code": 200,
    "title": "httpbin.org",
    "response_time_ms": 7527,
    "technologies": ["Python", "React", "Swagger UI", "gunicorn:19.9.0", "jQuery"],
    "fingerprints": ["swagger"],
    "asn_info": {
      "as_number": 14618, "as_org": "AMAZON-AES", "as_country": "US", "as_range": ["3.208.0.0/12"]
      },
    "tls_info": {
      "cert_issuer": "C=US, O=Amazon, CN=Amazon RSA 2048 M03",
      "cert_subject": "CN=httpbin.org",
      "tls_version": "TLSv1.2",
      "tls_cipher": "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
      "cert_san": [
        "httpbin.org",
        "*.httpbin.org"
      ]
    },
    "header": {
      "server": "gunicorn/19.9.0",
      "content-type": "text/html; charset=utf-8",
      "content-length": "9593",
      "connection": "keep-alive",
      "access-control-allow-origin": "*",
      "access-control-allow-credentials": "true"
    },
    "web_server": "gunicorn/19.9.0",
    "content_type": "text/html; charset=utf-8",
    "content_length": 9593,
    "tls_domain": "httpbin.org",
    "tls_probe_ip": "3.210.41.225",
    "redirect_url": "https://httpbin.org/",
    "html_urls": ["github.com", "fonts.googleapis.com", "kennethreitz.org"]
  }
]
```

### 示例1 同步快速调用(配置字典调用)

```python
import hprobe

# 核心配置
CORE_CONFIG = {
    # 目标支持ip/domain/url，示例：192.168.1.1/example.com/192.168.1.1:443/https://example.com
    "target": "example.com",  # 必选
    "ports": [80, 443],       # 可选：探测端口，不填则使用自动端口识别
    "timeout": 5.0,           # 可选：超时配置，默认10s
    "threads": 64,            # 可选：并发数配置，默认80
    "tls_info": True,         # 可选：开启TLS证书信息检测
    "asn": True,              # 可选：开启ASN归属查询
    "tech_detect": True,      # 可选：开启技术栈识别
    "fingerprint": True,       # 可选：开启Web指纹识别
    "silent": True,           # 可选：禁用命令行冗余日志
}

# 一行调用（字典接口，推荐）
result = hprobe.scan_target_with_config(CORE_CONFIG)
# 打印结果（返回字典，含所有探测信息）
print("探测结果：", result)
```

### 示例2 异步快速调用(配置字典调用)

```python
import asyncio
import hprobe

# 核心配置
CORE_CONFIG = {
    # 目标支持ip/domain/cidr/url
    # 示例：192.168.1.1、example.com、192.168.1.1:443、192.168.1.1/24、https://example.com
    "target": "192.168.1.1/24",  # 必选
    "ports": [80, 443],       # 可选：探测端口，不填则使用自动端口识别
    "timeout": 5.0,           # 可选：超时配置，默认10s
    "threads": 64,            # 可选：并发数配置，默认80
    "tls_info": True,         # 可选：开启TLS证书信息检测
    "asn": True,              # 可选：开启ASN归属查询
    "tech_detect": True,      # 可选：开启技术栈识别
    "fingerprint": True,      # 可选：开启Web指纹识别
    "silent": True,           # 可选：禁用命令行冗余日志
}

async def async_core_scan():
    # 异步字典接口调用
    result = await hprobe.scan_target_with_config_async(CORE_CONFIG)
    print("探测结果：", result)

# 执行异步函数并打印结果
asyncio.run(async_core_scan())

```

### 示例3 异步极简调用(链式调用)

```python
import hprobe
import asyncio

async def simple_async_scan():
    # 直接设置目标，其余用默认配置
    result = await hprobe.HprobeScanner().set_target("192.168.1.1/24").set_timeout(1.0).scan_async()
    print(f"扫描结果：共探测到{len(result)}个资产")
    # 遍历结果取值
    for asset in result:
        print(f"存活资产：{asset.get('url')}，状态码：{asset.get('status_code')}")

# 执行异步函数
asyncio.run(simple_async_scan())

```

### 示例4 同步极简调用(链式调用)

```python
import hprobe

# 同步链式调用
result = hprobe.HprobeScanner().set_target("httpbin.org").set_tech_detect(True).scan()
# 简单结果展示
if result:
    print(f"目标{result[0].get('target')}探测完成，技术栈：{result[0].get('technologies')}")

```

## ⚙️ 进阶参数配置说明

```python
# ⚠️ 可选：自定义数据目录
# import os
# os.environ["HPROBE_DATA_ROOT"] = r"C:\mydata\"

```

### 🔹 基础参数

- **`target`**  
  扫描目标，支持 IP 或域名

- **`ports`**  
  探测端口列表，例如：`[80, 443]`

- **`threads`**  
  并发线程数，用于控制整体并发规模

- **`timeout`**  
  单请求超时时间（单位：秒）

- **`methods`**  
  HTTP 请求方法：`GET` / `POST`

- **`scheme_policy`**  
  协议策略：`Auto` / `HTTP` / `HTTPS`

---

### 🔹 HTTP / 请求相关参数

- **`user_agent`**  
  自定义 User-Agent，默认使用内置随机

- **`max_redirects`**  
  最大重定向次数，设置为0则禁止重定向

- **`post_data`**  
  POST 请求体数据（字符串）

- **`post_file`**  
  POST 文件路径（与 `post_data` 二选一）

- **`content_type`**  
  POST 请求 Content-Type  
  默认值：`application/x-www-form-urlencoded`

---

### 🔹 功能开关（布尔值）

- **`asn`**  
  是否启用 ASN 查询

- **`tech_detect`**  
  是否启用技术栈识别

- **`fingerprint`**  
  是否启用 Web 指纹识别

- **`screenshot`**  
  是否启用网页截图

- **`common_ports`**  
  是否启用常见端口扫描

---
<!-- 
### 🔹 运行模式相关

- **`mode`**  
  运行模式：`active` / `passive`，默认主动检测，python端暂不支持被动检测

- **`response_file`**  
  被动模式响应文件（仅 `passive` 模式需要）

--- -->

### 🔹 其他参数

- **`silent`**  
  静默模式，仅输出结果，不打印日志

- **`dns`**  
  指定dns: [223.5.5.5,8.8.8.8]
  
- **`proxy`**  
  使用代理(http/https/socks)：socks5://127.0.0.1:1080

## 🖼 应用示例 / Example

以下是 **"PSX幻影网络空间测绘引擎"** 在 Windows 生产环境中 hprobe 的表现：

无GC抖动，运行稳定。

### 系统资源占用（实测）

- **CPU 占用**：5%–10%  
- **内存占用**：50 MB 左右  
- **启用 ASN查询**：内存占用约 100 MB
- **启用 wappalyzer/指纹规则查询后**：内存占用约 100–300 MB (随规则命中数缓慢递增)  

![Hprobe Screenshot](assets/psx.png)

注：图片中CPU和内存占用报告为系统整体占用报告(包含了浏览器/微信等其他应用资源的占用)

## License 📄 | 许可证

Copyright (c) 2026 FlyfishSec
All rights reserved.
