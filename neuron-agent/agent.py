"""Neuron Agent — 分布式神经元节点。

该进程代表一个区域中的神经元节点：启动时向编排器注册，之后每隔
HEARTBEAT_INTERVAL 秒向编排器的 /heartbeat 接口上报状态与脉冲值。

通过环境变量控制：
  REGION            区域标识（如 cn-north / us-east），默认 demo
  ORCHESTRATOR_URL  编排器地址，默认 http://localhost:8000
  HEARTBEAT_INTERVAL 心跳间隔秒数，默认 3
  NODE_ID           可选，指定稳定 node_id，不填则自动生成
  LOG_FILE          可选，日志输出到文件，默认空则只输出到 stdout
"""
import os
import sys
import time
import random
import socket
import uuid
import logging
import requests

ORCHESTRATOR_URL = os.environ.get("ORCHESTRATOR_URL", "http://localhost:8000")
REGION = os.environ.get("REGION", "demo")
HEARTBEAT_INTERVAL = float(os.environ.get("HEARTBEAT_INTERVAL", "3"))
NODE_ID = os.environ.get(
    "NODE_ID",
    f"neuron-{REGION}-{socket.gethostname()}-{uuid.uuid4().hex[:8]}",
)
LOG_FILE = os.environ.get("LOG_FILE", "")

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8") if LOG_FILE
        else logging.StreamHandler(sys.stdout)
    ],
)
log = logging.getLogger(f"node[{REGION}/{NODE_ID}]")


def register():
    try:
        resp = requests.post(
            f"{ORCHESTRATOR_URL}/aip/v1/nodes/create",
            json={
                "region": REGION,
                "node_type": "NEURON",
                "count": 1,
                "node_id": NODE_ID,
            },
            timeout=5,
        )
        resp.raise_for_status()
        log.info("注册成功: %s", resp.json())
        return True
    except Exception as exc:
        log.error("注册失败: %s", exc)
        return False


def heartbeat():
    pulse = round(random.uniform(0.1, 0.9), 3)
    try:
        resp = requests.post(
            f"{ORCHESTRATOR_URL}/aip/v1/nodes/heartbeat",
            json={
                "node_id": NODE_ID,
                "region": REGION,
                "node_type": "NEURON",
                "pulse": pulse,
            },
            timeout=5,
        )
        resp.raise_for_status()
        log.info("心跳 ok | pulse=%.3f", pulse)
    except Exception as exc:
        log.warning("心跳失败: %s", exc)


def main():
    log.info(
        "启动 node=%s region=%s orchestrator=%s heartbeat=%ss",
        NODE_ID, REGION, ORCHESTRATOR_URL, HEARTBEAT_INTERVAL,
    )

    # 持续尝试注册直到成功（编排器可能尚未就绪）
    for attempt in range(1, 21):
        if register():
            break
        log.info("等待编排器就绪... (%d/20)", attempt)
        time.sleep(2)
    else:
        log.error("无法注册到编排器，退出")
        sys.exit(1)

    # 心跳循环
    while True:
        heartbeat()
        time.sleep(HEARTBEAT_INTERVAL)


if __name__ == "__main__":
    main()
