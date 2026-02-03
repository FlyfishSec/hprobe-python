# Hprobe 🚀 [![PyPI Downloads](https://static.pepy.tech/personalized-badge/hprobe?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://github.com/FlyfishSec/hprobe)

A high-performance HTTP probing tool for asset discovery.

`hprobe` 是一个高性能 HTTP 探测引擎，基于 Rust 实现，并通过 Python 提供简单易用接口。
它支持同步和异步调用，能够快速探测目标 HTTP 服务、端口、指纹等，适用于大规模资产发现/网络空间测绘。

- 跨平台（Linux / Windows / macOS）  
- 支持多线程和异步模式  
- 可统一全局配置，方便批量调用  
- 提供参数化和字典配置两种接口

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

下面示例展示了 同步调用 和 异步调用，以及两种调用方式：参数化接口和字典接口。

```bash
import os
import asyncio
import hprobe

# -------------------------------
# 全局唯一配置（所有方法共用）
# -------------------------------
UNIFIED_CONFIG = {
    "target": "192.168.1.1",      # 统一目标
    "ports": [80],                # 统一端口
    "threads": 80,
    "timeout": 5.0,
    "max_redirects": 3,
    "methods": "GET",
    "scheme_policy": "Auto",
    "user_agent": None,
    "asn": False,
    "tech_detect": False,
    "fingerprint": False,
    "screenshot": False,
    "common_ports": False,
    "silent": True,
    "dns": [],
    "proxy": None,
    "post_data": None,
    "post_file": None,
    "content_type": "application/x-www-form-urlencoded",
    "mode": "active",
    "response_file": None,  # 被动模式响应文件，仅 passive 模式需配置
}

# ⚠️ 可选：自定义数据目录
# import os
# os.environ["HPROBE_DATA_ROOT"] = r"C:\mydata\"

# 1. 同步调用
def sync_scan_demo():
    print("="*60)
    print("【同步调用】参数化接口")
    print("="*60)
    result1 = hprobe.scan_target(**UNIFIED_CONFIG)
    print(f"结果: {result1 if result1 else '无有效结果'}\n")

    print("="*60)
    print("【同步调用】配置字典接口")
    print("="*60)
    result2 = hprobe.scan_target_with_config(UNIFIED_CONFIG)
    print(f"结果: {result2 if result2 else '无有效结果'}\n")

# 2. 异步调用
async def async_scan_demo():
    print("="*60)
    print("【异步调用】参数化接口")
    print("="*60)
    result1 = await hprobe.scan_target_async(**UNIFIED_CONFIG)
    print(f"结果: {result1 if result1 else '无有效结果'}\n")

    print("="*60)
    print("【异步调用】配置字典接口")
    print("="*60)
    result2 = await hprobe.scan_target_with_config_async(UNIFIED_CONFIG)
    print(f"结果: {result2 if result2 else '无有效结果'}\n")

# 3. 主函数示例
def main():
    run_sync = True
    run_async = True

    if run_sync:
        sync_scan_demo()

    if run_async:
        asyncio.run(async_scan_demo())

if __name__ == "__main__":
    main()
    print("="*60)
    print("所有扫描任务执行完成！")
    print("="*60)

```


## ⚙️ 参数配置说明

> 所有同步 / 异步接口共用以下参数配置

---

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
  自定义 User-Agent，默认使用内置值

- **`max_redirects`**  
  最大重定向次数

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

### 🔹 运行模式相关

- **`mode`**  
  运行模式：`active` / `passive`

- **`response_file`**  
  被动模式响应文件（仅 `passive` 模式需要）

---

### 🔹 其他参数

- **`silent`**  
  静默模式，仅输出结果，不打印日志

- **`dns`**  
  指定dns: [223.5.5.5,8.8.8.8]
  
- **`proxy`**  
  指定代理：socks5://127.0.0.1:1080

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
