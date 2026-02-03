import asyncio
import hprobe

# ======================
# 全局统一配置
# ======================
# 自定义环境变量配置，默认不需要，除非你有需求
# HPROBE_DATA_ROOT = os.getenv("HPROBE_DATA_ROOT", "c:\mydata\")
# import os
# os.environ["HPROBE_DATA_ROOT"] = HPROBE_DATA_ROOT

UNIFIED_CONFIG = {
    "target": "192.168.1.1",
    "ports": [80],
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
    "post_data": None,  # 无 POST 提交数据
    "post_file": None,  # 无从文件读取 POST 数据（与 post_data 互斥）
    "content_type": "application/x-www-form-urlencoded",  # Rust 端默认 Content-Type
    "mode": "active",  # Rust 端默认运行模式（主动探测）
    "response_file": None,  # 被动模式响应文件，默认无（仅 passive 模式需配置）
}


# ======================
# 1. 同步调用函数
# ======================
def sync_scan_demo():
    print("=" * 60)
    print("【同步调用】参数化接口")
    print("=" * 60)

    try:
        # 参数化接口：直接解包统一配置
        result1 = hprobe.scan_target(**UNIFIED_CONFIG)
        print(f"结果: {result1 if result1 else '无有效结果'}\n")
    except Exception as e:
        print(f"调用出错: {e}\n")

    print("=" * 60)
    print("【同步调用】配置字典接口")
    print("=" * 60)

    try:
        # 字典接口：直接传入统一配置
        result2 = hprobe.scan_target_with_config(UNIFIED_CONFIG)
        print(f"结果: {result2 if result2 else '无有效结果'}\n")
    except Exception as e:
        print(f"调用出错: {e}\n")


# ======================
# 2. 异步调用函数
# ======================
async def async_scan_demo():
    print("=" * 60)
    print("【异步调用】参数化接口")
    print("=" * 60)

    try:
        result1 = await hprobe.scan_target_async(**UNIFIED_CONFIG)
        print(f"结果: {result1 if result1 else '无有效结果'}\n")
    except Exception as e:
        print(f"调用出错: {e}\n")

    print("=" * 60)
    print("【异步调用】配置字典接口")
    print("=" * 60)

    try:
        result2 = await hprobe.scan_target_with_config_async(UNIFIED_CONFIG)
        print(f"结果: {result2 if result2 else '无有效结果'}\n")
    except Exception as e:
        print(f"调用出错: {e}\n")


# ======================
# 主函数
# ======================
def main():
    run_sync = True
    run_async = True

    if run_sync:
        sync_scan_demo()
        print("-" * 80 + "\n")

    if run_async:
        # if os.name == 'nt':
        #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        try:
            if run_async:
                asyncio.run(async_scan_demo())
                print("-" * 80 + "\n")
        except Exception as e:
            print(f"异步总入口出错: {e}")


if __name__ == "__main__":
    main()
    print("=" * 60)
    print("所有扫描任务执行完成！")
    print("=" * 60)