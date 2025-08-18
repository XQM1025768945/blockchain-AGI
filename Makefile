# 全球脑大模型 Makefile

# Python解释器
PYTHON = python

# 安装依赖
install:
	$(PYTHON) -m pip install -r requirements.txt

# 运行主程序
run:
	$(PYTHON) main.py

# 运行测试
test:
	$(PYTHON) main.py --test

# 运行示例
example:
	$(PYTHON) example.py

# 清理临时文件
clean:
	rm -rf temp/*
	rm -rf install/*
	rm -rf logs/*

# 帮助信息
help:
	@echo "全球脑大模型 Makefile"
	@echo ""
	@echo "可用命令:"
	@echo "  install  - 安装依赖"
	@echo "  run      - 运行主程序"
	@echo "  test     - 运行测试"
	@echo "  example  - 运行示例"
	@echo "  clean    - 清理临时文件"
	@echo "  help     - 显示帮助信息"

# 默认目标
.DEFAULT_GOAL := help