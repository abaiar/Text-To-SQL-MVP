# Text-to-SQL AI Agent

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.0+-green.svg)](https://langchain-ai.github.io/langgraph/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个基于大语言模型的智能 Text-to-SQL 转换系统，能够将自然语言查询自动转换为准确的 MySQL SQL 语句并执行。

## 项目概述

本项目是一个智能数据库查询代理（AI Agent），利用阿里云通义千问大模型（Qwen）和 LangGraph 框架，实现了从自然语言到 SQL 的自动转换。系统能够理解用户的查询意图，自动探索数据库结构，生成优化的 SQL 查询，并返回结构化的查询结果。

### 核心特性

- **自然语言理解**：准确解析用户的自然语言查询意图
- **智能数据库探索**：自动发现表结构、字段类型、主外键关系
- **SQL 自动生成**：基于数据库 Schema 生成标准 MySQL 语句
- **语法验证机制**：执行前自动验证 SQL 语法正确性
- **查询结果格式化**：以表格形式展示查询结果
- **安全执行策略**：防止 SQL 注入，支持只读查询模式

## 技术栈

| 组件 | 技术选型 | 用途 |
|------|----------|------|
| LLM | 阿里云通义千问 (Qwen) | 自然语言理解与 SQL 生成 |
| Agent 框架 | LangGraph | 智能体工作流编排 |
| 数据库 | MySQL | 数据存储与查询 |
| ORM | SQLAlchemy | 数据库连接与操作 |
| 日志 | Loguru | 结构化日志记录 |
| 配置管理 | python-dotenv | 环境变量管理 |

## 项目结构

```
Text-To-SQL-MVP/
├── src/
│   └── agent/
│       ├── agent.py              # 主代理入口，定义系统提示和工具编排
│       ├── my_llms.py            # LLM 配置（通义千问）
│       ├── tools/
│       │   ├── __init__.py
│       │   └── test_to_sql_tools.py  # 核心工具集定义
│       └── utils/
│           ├── __init__.py
│           ├── db_utils.py       # MySQL 数据库管理类
│           └── log_utils.py      # 日志工具类
├── pyproject.toml                # 项目依赖配置
├── langgraph.json                # LangGraph 部署配置
├── .env.example                  # 环境变量示例文件（复制为 .env 后使用）
├── .env                          # 环境变量（需自行创建，已加入 .gitignore）
├── .gitignore                    # Git 忽略规则
└── README.md                     # 项目文档
```

## 环境配置

### 前置要求

- Python >= 3.11
- MySQL 数据库
- 阿里云 DashScope API Key

### 安装步骤

1. **克隆仓库**

```bash
git clone <repository-url>
cd Text-To-SQL-MVP
```

2. **创建虚拟环境**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. **安装依赖**

```bash
pip install -e ".[dev]"
```

4. **配置环境变量**

项目使用 `.env` 文件管理环境变量。我们提供了一个示例文件 `.env.example`，您需要将其复制为 `.env` 并填写实际值。

**复制配置文件：**

```bash
# Linux/Mac
cp .env.example .env

# Windows
copy .env.example .env
```

**编辑 `.env` 文件，填写以下必需的环境变量：**

| 变量名 | 必填 | 说明 | 获取方式 |
|--------|------|------|----------|
| `DASHSCOPE_API_KEY` | ✅ | 阿里云 DashScope API Key | [DashScope 控制台](https://dashscope.aliyun.com/) |
| `DB_HOST` | ✅ | MySQL 数据库主机地址 | 数据库管理员提供 |
| `DB_PORT` | ✅ | MySQL 数据库端口 | 默认 3306 |
| `DB_NAME` | ✅ | MySQL 数据库名称 | 数据库管理员提供 |
| `DB_USER` | ✅ | MySQL 数据库用户名 | 数据库管理员提供 |
| `DB_PASSWORD` | ✅ | MySQL 数据库密码 | 数据库管理员提供 |
| `LANGSMITH_API_KEY` | ❌ | LangSmith API Key（可选，用于调试） | [LangSmith](https://smith.langchain.com/) |
| `LANGSMITH_TRACING` | ❌ | 是否启用追踪（true/false） | 默认为 false |
| `LANGSMITH_PROJECT` | ❌ | LangSmith 项目名称 | 自定义 |

**配置示例：**

```env
# LLM API 配置（必需）
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 数据库配置（必需）
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=my_database
DB_USER=root
DB_PASSWORD=my_secure_password

# LangSmith 配置（可选）
LANGSMITH_API_KEY=lsv2_pt_xxxxxxxxxxxxxxxx
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=text-to-sql-agent
```

> ⚠️ **安全提示**：
> - `.env` 文件包含敏感信息，**切勿**将其提交到版本控制
> - 项目已配置 `.gitignore` 自动忽略 `.env` 文件
> - 生产环境请使用更安全的密钥管理方式（如密钥管理服务）

## 使用指南

### 快速开始

#### 方式一：作为 LangGraph 应用运行

```bash
langgraph dev
```

访问 `http://localhost:2024` 即可通过 Web 界面与 Agent 交互。

#### 方式二：作为 Python 模块使用

```python
from agent.agent import agent
from langchain_core.messages import HumanMessage

# 发送自然语言查询
response = agent.invoke({
    "messages": [HumanMessage(content="查询所有用户的信息")]
})

print(response)
```

#### 方式三：测试工具集

```bash
# 测试数据库工具
python src/agent/utils/db_utils.py

# 测试 SQL 工具集
python src/agent/tools/test_to_sql_tools.py
```

### 使用示例

#### 示例 1：简单查询

**用户输入**：
```
查询所有用户的信息
```

**Agent 执行流程**：
1. 调用 `list_tables()` 发现 `users` 表
2. 调用 `get_table_schema("users")` 获取表结构
3. 生成并执行 SQL：
```sql
SELECT id, username, email, created_at 
FROM users 
LIMIT 100;
```

#### 示例 2：条件查询

**用户输入**：
```
查找最近 30 天内注册的高级会员
```

**生成的 SQL**：
```sql
SELECT 
    id, 
    username, 
    email, 
    vip_level,
    created_at
FROM users
WHERE vip_level >= 2
  AND created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY created_at DESC;
```

#### 示例 3：聚合统计

**用户输入**：
```
统计每个分类的商品数量和平均价格
```

**生成的 SQL**：
```sql
SELECT 
    category,
    COUNT(*) as product_count,
    ROUND(AVG(price), 2) as avg_price,
    MIN(price) as min_price,
    MAX(price) as max_price
FROM products
WHERE status = 'active'
GROUP BY category
ORDER BY product_count DESC;
```

## 核心工具说明

| 工具名称 | 功能描述 | 使用场景 |
|----------|----------|----------|
| `list_tables` | 列出数据库所有表 | 了解数据库结构 |
| `get_table_schema` | 获取指定表的结构信息 | 查询前了解字段详情 |
| `check_sql_query` | 验证 SQL 语法 | 执行前确保语法正确 |
| `execute_sql_query` | 执行 SQL 查询 | 获取查询结果 |

## 开发规范

### 代码风格

本项目使用 Ruff 进行代码格式化和检查：

```bash
# 格式化代码
ruff format .

# 检查代码
ruff check .

# 类型检查
mypy src/
```

### 提交规范

- 遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范
- 提交前确保代码通过所有检查
- 敏感信息（API Key、密码等）不得提交到版本控制

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

本项目采用 [MIT](LICENSE) 许可证开源。

## 维护者

- **赵健硕** - [18853577985@126.com](mailto:18853577985@126.com)

## 致谢

- [LangChain](https://python.langchain.com/) - LLM 应用开发框架
- [LangGraph](https://langchain-ai.github.io/langgraph/) - Agent 工作流编排
- [阿里云通义千问](https://tongyi.aliyun.com/) - 大语言模型支持

---

**注意**：本项目仅供学习和研究使用，生产环境部署时请注意数据安全和权限控制。
