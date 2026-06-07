from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import time
import os
import random
from collections import Counter
from typing import Optional, Dict, Any, List

app = FastAPI(title="Global Neural Brain - AI Orchestrator")

# CORS —— 允许前端从不同端口/域名访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- 全局状态 ----------
nodes: Dict[str, Any] = {}
tasks: Dict[str, Any] = {}
event_log: List[Dict[str, Any]] = []
START_TS = int(time.time())

# 心跳 TTL：超过此秒数无心跳 -> OFFLINE；再超过此时间 -> 删除
HEARTBEAT_TTL = 15
OFFLINE_TTL = 120

# 支持的区域坐标（用于前端地图渲染）
REGION_COORDS = {
    "cn-north": {"lat": 39.9042, "lon": 116.4074, "label": "华北 (Beijing)"},
    "cn-east": {"lat": 31.2304, "lon": 121.4737, "label": "华东 (Shanghai)"},
    "cn-south": {"lat": 23.1291, "lon": 113.2644, "label": "华南 (Guangzhou)"},
    "cn-west": {"lat": 30.5728, "lon": 104.0668, "label": "华西 (Chengdu)"},
    "us-east": {"lat": 40.7128, "lon": -74.0060, "label": "美东 (New York)"},
    "us-west": {"lat": 37.7749, "lon": -122.4194, "label": "美西 (San Francisco)"},
    "eu-west": {"lat": 51.5074, "lon": -0.1278, "label": "欧洲 (London)"},
    "ap-southeast": {"lat": 1.3521, "lon": 103.8198, "label": "新加坡 (Singapore)"},
    "ap-northeast": {"lat": 35.6762, "lon": 139.6503, "label": "日本 (Tokyo)"},
    "demo": {"lat": 0.0, "lon": 0.0, "label": "Demo"},
}


def push_event(event_type: str, payload: Dict[str, Any]):
    """保留最近 200 条事件日志用于前端展示"""
    event_log.append(
        {
            "type": event_type,
            "ts": int(time.time()),
            **payload,
        }
    )
    if len(event_log) > 200:
        event_log.pop(0)


def upsert_node(node_id: str, region: str, node_type: str = "NEURON",
                pulse: Optional[float] = None):
    now = int(time.time())
    is_new = node_id not in nodes
    if is_new:
        nodes[node_id] = {
            "id": node_id,
            "type": node_type,
            "region": region,
            "status": "ONLINE",
            "pulse": pulse if pulse is not None else round(random.uniform(0.1, 0.9), 3),
            "ts": now,
            "last_seen": now,
        }
        push_event("node_created", {"node_id": node_id, "region": region})
    else:
        node = nodes[node_id]
        prev_status = node["status"]
        node["last_seen"] = now
        if pulse is not None:
            node["pulse"] = pulse
        if prev_status != "ONLINE":
            node["status"] = "ONLINE"
            push_event("node_online", {"node_id": node_id, "region": region})


# ---------- 请求模型 ----------
class CreateNodesReq(BaseModel):
    region: str
    node_type: str = "NEURON"
    count: int = 1
    node_id: Optional[str] = None  # 允许客户端指定稳定 node_id
    auto_propagate: bool = True


class HeartbeatReq(BaseModel):
    node_id: str
    region: str
    node_type: str = "NEURON"
    pulse: Optional[float] = None


# ---------- 根入口 ----------
@app.get("/")
def root():
    return {
        "name": "Global Neural Brain - AI Orchestrator",
        "version": "v0.1.0",
        "status": "running",
        "docs": "/docs",
        "dashboard": "/dashboard/",
        "endpoints": {
            "nodes": {
                "create": "/aip/v1/nodes/create",
                "destroy": "/aip/v1/nodes/destroy",
                "status": "/aip/v1/nodes/status",
                "heartbeat": "/aip/v1/nodes/heartbeat",
            },
            "learning": {"submit": "/aip/v1/learning/submit"},
            "model": {"status": "/aip/v1/model/status"},
            "metrics": "/aip/v1/metrics",
            "websocket": "/ws/spike",
        },
    }


# ---------- 节点管理 ----------
@app.post("/aip/v1/nodes/create")
def create_nodes(req: CreateNodesReq):
    task_id = f"task-{int(time.time())}"
    tasks[task_id] = {"status": "RUNNING", "msg": f"创建 {req.count} 神经元节点"}
    for i in range(req.count):
        if req.node_id and req.count == 1:
            node_id = req.node_id
        else:
            node_id = f"neuron-{req.region}-{i}-{int(time.time()) % 1000}"
        upsert_node(node_id, req.region, req.node_type)
    tasks[task_id]["status"] = "SUCCESS"
    return {"task_id": task_id, "status": "SUCCESS"}


@app.post("/aip/v1/nodes/heartbeat")
def heartbeat(req: HeartbeatReq):
    upsert_node(req.node_id, req.region, req.node_type, req.pulse)
    return {
        "ok": True,
        "node_id": req.node_id,
        "region": req.region,
        "server_ts": int(time.time()),
    }


@app.post("/aip/v1/nodes/destroy")
def destroy_nodes(node_ids: List[str]):
    removed = 0
    for nid in node_ids:
        if nid in nodes:
            del nodes[nid]
            removed += 1
            push_event("node_destroyed", {"node_id": nid})
    return {"success": True, "removed": removed, "msg": "节点已销毁"}


@app.get("/aip/v1/nodes/status")
def get_nodes(region: Optional[str] = None, node_type: Optional[str] = None):
    result = list(nodes.values())
    if region:
        result = [n for n in result if n["region"] == region]
    if node_type:
        result = [n for n in result if n["type"] == node_type]
    return {"nodes": result}


@app.post("/aip/v1/learning/submit")
def submit_learning(task_type: str = "EDGE_DISTILL", region: str = "global"):
    task_id = f"learn-{int(time.time())}"
    tasks[task_id] = {"status": "STARTED", "type": task_type, "region": region}
    push_event("learning", {"task_id": task_id, "type": task_type, "region": region})
    return {"task_id": task_id, "status": "STARTED"}


@app.get("/aip/v1/model/status")
def model_status():
    return {"version": "v0.1.0", "accuracy": round(random.uniform(0.85, 0.95), 3)}


# ---------- 聚合 metrics ----------
@app.get("/aip/v1/metrics")
def get_metrics():
    region_counter = Counter(n["region"] for n in nodes.values())
    type_counter = Counter(n["type"] for n in nodes.values())
    status_counter = Counter(n["status"] for n in nodes.values())
    regions = []
    for region, count in region_counter.items():
        coord = REGION_COORDS.get(
            region, {"lat": 0.0, "lon": 0.0, "label": region}
        )
        avg_pulse = 0.0
        region_nodes = [n for n in nodes.values() if n["region"] == region]
        if region_nodes:
            avg_pulse = round(
                sum(n["pulse"] for n in region_nodes) / len(region_nodes), 3
            )
        regions.append(
            {
                "region": region,
                "label": coord.get("label", region),
                "lat": coord.get("lat", 0.0),
                "lon": coord.get("lon", 0.0),
                "count": count,
                "avg_pulse": avg_pulse,
            }
        )
    uptime = int(time.time()) - START_TS
    return {
        "total_nodes": len(nodes),
        "online_nodes": status_counter.get("ONLINE", 0),
        "offline_nodes": status_counter.get("OFFLINE", 0),
        "regions": regions,
        "by_type": dict(type_counter),
        "by_status": dict(status_counter),
        "uptime_seconds": uptime,
        "recent_events": event_log[-30:],
        "ts": int(time.time()),
    }


# ---------- 离线检测后台任务 ----------
async def offline_monitor():
    while True:
        await asyncio.sleep(5)
        now = int(time.time())
        to_delete = []
        for node_id, node in nodes.items():
            last_seen = node.get("last_seen", node.get("ts", 0))
            age = now - last_seen
            if age > HEARTBEAT_TTL and node["status"] == "ONLINE":
                node["status"] = "OFFLINE"
                push_event(
                    "node_offline",
                    {"node_id": node_id, "region": node["region"]},
                )
            if age > OFFLINE_TTL:
                to_delete.append(node_id)
        for nid in to_delete:
            del nodes[nid]
            push_event("node_purged", {"node_id": nid})


# ---------- WebSocket 脉冲推送 ----------
@app.websocket("/ws/spike")
async def websocket_spikes(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(1)
        node_ids = [nid for nid, n in nodes.items() if n["status"] == "ONLINE"]
        if not node_ids:
            continue
        node_id = random.choice(node_ids)
        pulse = round(random.uniform(0.1, 0.9), 3)
        if node_id in nodes:
            nodes[node_id]["pulse"] = pulse
        await websocket.send_json(
            {"event": "spike", "node": node_id, "pulse": pulse, "ts": time.time()}
        )


# ---------- FastAPI 生命周期 ----------
@app.on_event("startup")
async def _startup():
    asyncio.create_task(offline_monitor())


# ---------- 静态文件托管（前端仪表盘） ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")
os.makedirs(DASHBOARD_DIR, exist_ok=True)
app.mount(
    "/dashboard",
    StaticFiles(directory=DASHBOARD_DIR, html=True),
    name="dashboard",
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
