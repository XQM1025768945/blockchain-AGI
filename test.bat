@echo off

REM 全球脑大模型测试脚本

REM 检查是否安装了Python
echo 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

echo Python环境检查通过

REM 检查依赖
echo 检查项目依赖...
if not exist "requirements.txt" (
    echo 错误: 未找到requirements.txt文件
    pause
    exit /b 1
)

echo 依赖文件检查通过

REM 安装依赖
echo 安装项目依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)

echo 依赖安装完成

REM 运行测试
echo 运行测试...
python main.py --test

pause