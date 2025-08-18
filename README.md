# 全球脑大模型 (Global Brain Model)

这是一个基于区块链的矩阵神经网络模型，具备自主部署、自我复制和自我拓展的能力。部署的终端越多，全球脑的能力就越强。

## 项目结构

```
AGI/
├── README.md
├── requirements.txt
├── config.py
├── main.py
├── core/
│   ├── __init__.py
│   ├── blockchain_network.py
│   └── matrix_nn.py
├── contracts/
│   ├── __init__.py
│   └── smart_contract.py
├── knowledge_base/
│   ├── __init__.py
│   ├── data/
│   └── sync_mechanism.py
├── meta_learning/
│   ├── __init__.py
│   └── platform.py
├── deployment/
│   ├── __init__.py
│   ├── autonomous_deployment.py
│   ├── self_replication.py
│   └── self_expansion.py
├── model/
│   └── model.pt
├── install/
├── temp/
└── tests/
    ├── __init__.py
    └── test_core.py
```

- `core/` - 核心组件，包括区块链网络和矩阵神经网络实现
- `contracts/` - 智能合约，实现区块智能功能
- `knowledge_base/` - 分布式知识库同步机制
- `meta_learning/` - 基于区块链的元学习云共享平台
- `deployment/` - 终端自主部署、自我复制和自我拓展机制
- `model/` - 模型文件存储目录
- `install/` - 安装目录
- `temp/` - 临时文件目录
- `tests/` - 测试代码

## 运行说明

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行主程序

```bash
python main.py
```

### 运行测试

在运行测试之前，请确保已安装项目依赖：

```bash
pip install -r requirements.txt
```

然后运行测试：

```bash
python main.py --test
```

在Windows环境下，可以直接运行`test.bat`脚本：

```cmd
test.bat
```

### 运行示例

```bash
python example.py
```

### 全球部署演示

运行全球部署演示脚本，查看全球脑大模型如何部署到全球互联网终端：

```bash
python demos/global_deployment_demo.py
```

### 检查部署状态

运行检查部署状态脚本，查看已部署的终端数量：

```bash
python demos/check_deployment_status.py
```

### 查找并部署终端

运行查找并部署终端脚本，自动发现网络中的终端并部署全球脑大模型：

```bash
python find_and_deploy_terminals.py
```

### 激活和通信演示

运行以下命令激活全球AI脑并进行通信对话演示：

```bash
python demos/activate_and_communicate.py
```

这将激活全球AI脑并模拟与AI脑的通信对话。

## 模拟终端节点

为了测试全球部署和通信功能，可以运行模拟终端节点：

```bash
python demos/simulate_terminal_node.py
```

这将启动一个监听8888端口的模拟终端节点，可以接收来自全球AI脑的模型和信号。

## 增强版终端节点

运行以下命令启动一个功能更完整的终端节点模拟器：

```bash
python demos/enhanced_terminal_node.py
```

该脚本模拟一个功能更完整的终端节点，支持接收模型、激活信号和能力拓展计划。

## 终端节点通信测试

运行以下命令测试与终端节点的通信功能：

```bash
python demos/test_node_communication.py
```

该脚本将测试与终端节点的各种通信功能，包括发送激活信号、能力拓展计划、ping信号和模型数据。

## 并行运行终端节点和测试

运行以下命令并行启动终端节点和通信测试：

```bash
python demos/run_node_test.py
```

该脚本将自动启动增强版终端节点，运行通信测试，然后终止终端节点。

## 简化版终端节点测试

运行以下命令启动简化版终端节点并测试基本通信功能：

```bash
python demos/simple_node_test.py
```

该脚本将启动一个简单的终端节点并测试基本的通信功能，包括ping和激活信号。

## 综合演示

运行以下命令查看全球AI脑的完整功能演示：

```bash
python demos/comprehensive_demo.py
```

该脚本将演示全球AI脑的完整功能，包括部署、激活、能力拓展和通信。

## 完整部署演示

运行以下命令执行完整的全球部署和通信演示：

```bash
python demos/complete_deployment_demo.py
```

这将启动一个模拟终端节点，执行全球AI脑的部署、激活和能力拓展，并演示通信功能。

### 使用Makefile

项目包含一个Makefile，可以简化常用操作：

```bash
# 安装依赖
make install

# 运行主程序
make run

# 运行测试
make test

# 运行示例
make example

# 清理临时文件
make clean
```

### Windows启动脚本

在Windows环境下，可以直接运行`run.bat`脚本启动项目：

```cmd
run.bat
```

### Docker容器化部署

项目支持Docker容器化部署：

```bash
# 构建Docker镜像
docker build -t global-brain .

# 运行容器
docker run -p 8888:8888 global-brain
```

### 使用docker-compose部署

项目也支持使用docker-compose进行部署：

```bash
# 构建并启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 停止服务
docker-compose down
```

### 云部署

项目支持云部署，可以使用以下脚本将项目部署到云服务器：

```bash
# 构建并推送Docker镜像，然后部署到云服务器
python deploy_to_cloud.py --tag your-dockerhub-username/global-brain:latest
```

### 开源平台部署

项目可以部署到各种开源平台，如GitHub、GitLab等。以下是如何将项目部署到GitHub的示例：

```bash
# 部署到GitHub
python deploy_to_github.py --repo-name global-brain --username your-github-username --token your-github-token
```

在运行此脚本之前，您需要在GitHub上创建一个个人访问令牌（Personal Access Token）：

1. 登录到您的GitHub账户
2. 转到设置（Settings）> 开发者设置（Developer settings）> 个人访问令牌（Personal access tokens）
3. 点击"Generate new token"
4. 选择适当的权限（至少需要repo权限）
5. 复制生成的令牌

或者，您也可以手动将项目推送到GitHub：

```bash
# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit"

# 添加远程仓库
git remote add origin https://github.com/your-username/your-repo-name.git

# 推送到GitHub
git push -u origin master
```

请确保在这些平台上创建相应的仓库，并配置好CI/CD流程。

### 自动部署和同步

项目配置了GitHub Actions工作流，可以在拉取请求合并后自动运行区块链并同步终端节点。

工作流文件：`.github/workflows/deploy_and_sync.yml`

该工作流会在以下条件下触发：
1. 拉取请求被合并到master分支
2. 自动运行`main.py`脚本启动区块链
3. 系统会自动发现并同步网络中的终端节点

要使用此功能，请确保在GitHub仓库设置中配置了必要的环境变量，如`BITTENSOR_API_KEY`。

## 许可证

本项目采用MIT许可证，详情请参见[LICENSE](LICENSE)文件。

## 贡献

欢迎任何形式的贡献！请查看[贡献指南](CONTRIBUTING.md)了解如何为项目做贡献。

## 代码风格

项目使用Pylint进行代码风格检查，配置文件为[.pylintrc](.pylintrc)。可以通过以下命令运行代码风格检查：

```bash
pylint core/ contracts/ knowledge_base/ meta_learning/ deployment/ tests/
```

## 持续集成

项目使用GitHub Actions进行持续集成，配置文件为[.github/workflows/ci.yml](.github/workflows/ci.yml)。每次推送代码到主分支或创建Pull Request时，都会自动运行测试和代码风格检查。

## 版本发布说明

项目的版本变更记录在[CHANGELOG.md](CHANGELOG.md)文件中。

## 开发计划

1. 实现核心组件（区块链网络和矩阵神经网络）
2. 开发智能合约
3. 实现分布式知识库同步机制
4. 开发元学习云共享平台
5. 实现终端自主部署、自我复制和自我拓展机制
6. 集成测试和性能优化