/* Global Neural Brain — 前端仪表盘
 * 数据源: /aip/v1/metrics, /aip/v1/nodes/status, /aip/v1/nodes/create
 * 实时流: /ws/spike (WebSocket)
 */

const API_BASE = "/aip/v1";

// ---------------- 经纬度 → SVG 坐标 ----------------
// viewBox 1000 x 500, 等距圆柱投影
// x = (lon + 180) / 360 * 1000
// y = (90 - lat) / 180 * 500
function project(lon, lat) {
  return {
    x: ((lon + 180) / 360) * 1000,
    y: ((90 - lat) / 180) * 500,
  };
}

// ---------------- 简化大陆轮廓（纯手工路径，近似示意） ----------------
// 使用低精度多边形表示各大洲。坐标以 (lon,lat) 对表示。
const CONTINENTS = [
  // 北美
  [[-160, 70], [-50, 70], [-55, 50], [-80, 25], [-100, 18], [-120, 32], [-135, 55], [-160, 60]],
  // 南美
  [[-80, 12], [-35, 12], [-40, -10], [-55, -35], [-70, -55], [-75, -20], [-80, 0]],
  // 欧洲
  [[-10, 60], [35, 60], [40, 50], [25, 40], [10, 40], [-10, 45]],
  // 非洲
  [[-15, 35], [50, 35], [52, 15], [45, -10], [30, -30], [15, -35], [10, -10], [-15, 15]],
  // 亚洲
  [[35, 70], [180, 70], [145, 50], [125, 30], [110, 20], [95, 10], [80, 25], [65, 25], [50, 40], [40, 55]],
  // 澳洲 / 大洋洲
  [[110, -10], [155, -10], [155, -38], [120, -38], [110, -25]],
];

function drawContinents() {
  const g = document.getElementById("continents");
  g.innerHTML = "";
  CONTINENTS.forEach((pts) => {
    const path = pts
      .map(([lon, lat]) => {
        const { x, y } = project(lon, lat);
        return `${x.toFixed(1)},${y.toFixed(1)}`;
      })
      .join(" ");
    const poly = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
    poly.setAttribute("points", path);
    g.appendChild(poly);
  });
}

// ---------------- 工具函数 ----------------
function fmtTime(ts) {
  const d = new Date(ts * 1000);
  const pad = (n) => String(n).padStart(2, "0");
  return `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
}

function fmtUptime(sec) {
  const h = Math.floor(sec / 3600);
  const m = Math.floor((sec % 3600) / 60);
  const s = sec % 60;
  return `${h}h ${m}m ${s}s`;
}

async function fetchJSON(path) {
  const res = await fetch(API_BASE + path);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// ---------------- 渲染 ----------------
function renderMetrics(data) {
  document.getElementById("metric-total").textContent = data.total_nodes || 0;
  document.getElementById("metric-online").textContent = data.online_nodes || 0;
  document.getElementById("metric-offline").textContent = data.offline_nodes || 0;
  document.getElementById("metric-regions").textContent =
    (data.regions || []).length;
  document.getElementById("uptime").textContent = fmtUptime(data.uptime_seconds || 0);
  document.getElementById("last-update").textContent = fmtTime(data.ts);

  // 区域列表
  const list = document.getElementById("region-list");
  list.innerHTML = "";
  (data.regions || []).forEach((r) => {
    const row = document.createElement("div");
    row.className = "region-item";
    row.innerHTML = `
      <div>
        <div class="title">${r.label}</div>
        <span class="meta">${r.region} · 脉冲均值 ${r.avg_pulse}</span>
      </div>
      <div style="text-align:right; font-weight:600;">${r.count} 节点</div>
      <div class="pulse-bar"><div style="width:${Math.min(100, r.avg_pulse * 100)}%"></div></div>
    `;
    list.appendChild(row);
  });

  // 事件流
  const stream = document.getElementById("event-stream");
  stream.innerHTML = "";
  (data.recent_events || []).slice().reverse().forEach((ev) => {
    const li = document.createElement("li");
    li.className = `type-${ev.type}`;
    li.innerHTML = `<span class="time">[${fmtTime(ev.ts)}]</span> ${ev.type} — ${
      JSON.stringify(ev).replace(/[{}"]/g, "")
    }`;
    stream.appendChild(li);
  });

  // 地图节点
  drawMapNodes(data.regions || []);

  // 区域下拉框
  const select = document.getElementById("region-select");
  const current = select.value;
  select.innerHTML = `<option value="">全部区域</option>` +
    (data.regions || [])
      .map((r) => `<option value="${r.region}">${r.label}</option>`)
      .join("");
  select.value = current;
}

function drawMapNodes(regions) {
  const nodesG = document.getElementById("nodes");
  nodesG.innerHTML = "";
  regions.forEach((r) => {
    const { x, y } = project(r.lon, r.lat);
    const radius = Math.min(4 + r.count * 1.5, 14);
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", x);
    circle.setAttribute("cy", y);
    circle.setAttribute("r", radius);
    circle.setAttribute("fill", "#22c55e");
    circle.setAttribute("fill-opacity", 0.35);
    circle.setAttribute("stroke", "#22c55e");
    circle.setAttribute("stroke-width", 1.2);
    circle.classList.add("node-marker");
    circle.setAttribute(
      "data-tip",
      `${r.label} · ${r.count} nodes · avg pulse ${r.avg_pulse}`
    );
    nodesG.appendChild(circle);

    // 标签
    const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    label.setAttribute("x", x + radius + 4);
    label.setAttribute("y", y + 4);
    label.classList.add("node-label");
    label.textContent = `${r.label} (${r.count})`;
    nodesG.appendChild(label);

    // 脉冲环
    const ring = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    ring.setAttribute("cx", x);
    ring.setAttribute("cy", y);
    ring.setAttribute("r", 3);
    ring.classList.add("pulse-ring");
    ring.style.animationDelay = `${Math.random() * 2}s`;
    nodesG.appendChild(ring);
  });

  // 为每个节点绑定 tooltip hover（简单 title）
  nodesG.querySelectorAll("circle.node-marker").forEach((el) => {
    el.addEventListener("mouseenter", () => {});
  });
}

async function renderNodesTable(filterRegion = "") {
  try {
    const data = await fetchJSON("/nodes/status" + (filterRegion ? `?region=${encodeURIComponent(filterRegion)}` : ""));
    const tbody = document.getElementById("node-table");
    tbody.innerHTML = "";
    (data.nodes || []).forEach((n) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${n.id}</td>
        <td>${n.region}</td>
        <td>${n.type}</td>
        <td><span class="status-badge ${n.status}">${n.status}</span></td>
        <td>${n.pulse ?? "-"}</td>
        <td>${fmtTime(n.ts)}</td>
      `;
      tbody.appendChild(tr);
    });
    if (!data.nodes || data.nodes.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:20px; color:var(--muted);">暂无节点</td></tr>`;
    }
  } catch (e) {
    console.error(e);
  }
}

// ---------------- 主循环 ----------------
let refreshTimer = null;
async function refresh() {
  try {
    setConn(true);
    const metrics = await fetchJSON("/metrics");
    renderMetrics(metrics);
    const selected = document.getElementById("region-select").value;
    renderNodesTable(selected);
  } catch (e) {
    console.error(e);
    setConn(false);
  }
}

function setConn(ok) {
  const dot = document.getElementById("conn-status");
  const lbl = document.getElementById("conn-label");
  dot.classList.toggle("online", ok);
  dot.classList.toggle("offline", !ok);
  lbl.textContent = ok ? "已连接" : "连接异常";
}

// ---------------- WebSocket 实时脉冲 ----------------
function connectWs() {
  const proto = location.protocol === "https:" ? "wss:" : "ws:";
  const ws = new WebSocket(`${proto}//${location.host}/ws/spike`);
  ws.onmessage = (evt) => {
    try {
      const msg = JSON.parse(evt.data);
      // 对收到的节点做一次视觉脉冲高亮
      flashNode(msg.node);
    } catch (_) {}
  };
  ws.onclose = () => {
    setTimeout(connectWs, 3000);
  };
}

function flashNode(nodeId) {
  // 简单做法：在 nodes 层加一个临时闪光圈
  const g = document.getElementById("pulses");
  // 从已知节点反推坐标（取 node 内的 circle.node-marker）
  const circles = document.querySelectorAll("#nodes circle.node-marker");
  // 按 id 匹配复杂，这里随机挑一个标记闪烁以体现实时性
  if (circles.length === 0) return;
  const target = circles[Math.floor(Math.random() * circles.length)];
  const cx = parseFloat(target.getAttribute("cx"));
  const cy = parseFloat(target.getAttribute("cy"));
  const flash = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  flash.setAttribute("cx", cx);
  flash.setAttribute("cy", cy);
  flash.setAttribute("r", 3);
  flash.setAttribute("fill", "url(#pulseGrad)");
  flash.style.opacity = "1";
  flash.style.transition = "all 1.2s ease-out";
  g.appendChild(flash);
  requestAnimationFrame(() => {
    flash.setAttribute("r", 40);
    flash.style.opacity = "0";
  });
  setTimeout(() => flash.remove(), 1300);
}

// ---------------- 交互按钮 ----------------
document.addEventListener("DOMContentLoaded", () => {
  drawContinents();
  refresh();
  refreshTimer = setInterval(refresh, 3000);
  connectWs();

  document.getElementById("btn-refresh").addEventListener("click", refresh);
  document.getElementById("region-select").addEventListener("change", (e) => {
    renderNodesTable(e.target.value);
  });

  document.getElementById("btn-create").addEventListener("click", async () => {
    const regions = [
      "cn-north", "cn-east", "cn-south", "cn-west",
      "us-east", "us-west", "eu-west",
      "ap-southeast", "ap-northeast",
    ];
    const region = regions[Math.floor(Math.random() * regions.length)];
    try {
      await fetch(API_BASE + "/nodes/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ region, count: 1 }),
      });
      refresh();
    } catch (e) {
      console.error(e);
    }
  });
});
