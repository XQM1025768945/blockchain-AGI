# 全球神经网络大脑 · 完整交付包

> 分布式全球类脑智能网络（中枢-边缘-神经元）完整项目，开箱即用。

---

## 两个交付版本

本项目提供两套交付物：

### 🚀 推荐：完整 Monorepo（推荐使用）

基于 `GSC_AGI.md` 完整方案构建的 Production-ready Monorepo，包含四大平面、完整 AIP 接口、AI 编排器全套模块。

**👉 进入：[global-neural-matrix/README.md](global-neural-matrix/README.md)**

```
global-neural-matrix/
├── api/                          # gRPC + REST + AsyncAPI（完整AIP）
├── orchestrator/                 # AI 编排器（感知+规划+执行+学习）
├── infra/                        # Terraform + Ansible
├── network/                      # libp2p + 传播代理 + 终端微内核
├── intelligence/                 # 联邦蒸馏 + GraphRAG + MLOps
├── security/                     # SPIFFE/SPIRE + Cosign
├── deployment/                   # Helm Charts + K8s
└── docs/                         # 架构文档
```

### 🔧 轻量原型（已验证可运行）

基于 FastAPI 的最小化原型，适合快速验证概念。

```
./
├── orchestrator/main.py           # AI 编排器（FastAPI）
├── neuron-agent/agent.py         # 终端神经元
├── spike-protocol/spike.py        # 脉冲编解码
├── aip/global_neural_brain.proto # AIP Proto
├── docker-compose.yml             # 一键启动
├── deploy/                       # 部署脚本
└── docs/                         # 立项书 + 白皮书
```

快速开始：

```bash
docker-compose up -d --build
# 访问 http://localhost:8000/docs
```

---

## 核心价值

1. **仿生结构**：模拟人类大脑分层拓扑、脉冲发放、稀疏连接
2. **AI 自治**：全自动部署、运维、学习、进化
3. **极低带宽**：仅传输脉冲，流量降低 100~1000 倍
4. **隐私原生**：联邦学习，数据不出终端
5. **开放生态**：AIP 标准接口，所有大型 AI 可接入管理

## 四大平面架构

| 平面 | 组件 | 说明 |
|------|------|------|
| 基础设施 | Terraform + Ansible | 节点自动化部署、零接触配置 |
| 网络 | libp2p + DHT + GossipSub | 自组织突触矩阵、脉冲广播 |
| 智能与数据 | 联邦蒸馏 + GraphRAG + MLOps | 两级蒸馏、知识图谱、自动流水线 |
| AI 编排器 | 感知→规划→执行→学习 | 元大脑，协调三平面并开放 AIP |

## 文档

- **完整技术方案**：[GSC_AGI.md](GSC_AGI.md)
- **项目立项书**：[docs/project_proposal.md](docs/project_proposal.md)
- **技术白皮书**：[docs/white_paper.md](docs/white_paper.md)
- **完整 Monorepo**：[global-neural-matrix/](global-neural-matrix/)

## 实施阶段

1. 2026-2028：原型验证
2. 2028-2030：区域组网
3. 2030-2035：功能脑区成型
4. 2035-2040：全球大脑觉醒
