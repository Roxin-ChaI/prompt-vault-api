# Prompt Vault API

[English](README.md) | [简体中文](README.zh-CN.md)

一个用于存储、搜索、更新和管理可复用提示词的 REST API。

本项目展示了一套完整的后端开发与交付流程，使用 FastAPI、SQLAlchemy、SQLite、Alembic、pytest、Ruff、Docker、Docker Compose 和 GitHub Actions。

## 功能

- 创建可复用提示词
- 查看全部提示词
- 根据 ID 获取提示词
- 更新已有提示词
- 删除提示词
- 根据标题或内容搜索提示词
- 根据标签筛选提示词
- 使用 SQLite 持久化数据
- 使用 Alembic 管理数据库结构变更
- 使用 pytest 运行自动化测试
- 使用 Ruff 检查代码质量
- 使用 Docker 运行应用
- 使用 GitHub Actions 执行持续集成

## 技术栈

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- Pydantic
- pytest
- Ruff
- Docker
- Docker Compose
- GitHub Actions

## 项目结构

```text
prompt-vault-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── database.py
│   ├── dependencies.py
│   ├── init_db.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── docs/
│   └── requirements.md
├── migrations/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── tests/
│   ├── conftest.py
│   ├── test_main.py
│   ├── test_schemas.py
│   └── test_search.py
├── .dockerignore
├── .gitignore
├── alembic.ini
├── compose.yaml
├── Dockerfile
├── pyproject.toml
├── README.md
└── README.zh-CN.md
```

## 本地开发

### 1. 创建虚拟环境

```bash
python3.12 -m venv .venv
```

### 2. 激活虚拟环境

在 macOS 或 Linux 上执行：

```bash
source .venv/bin/activate
```

### 3. 安装依赖

```bash
python -m pip install --upgrade pip
python -m pip install ".[dev]"
```

### 4. 执行数据库迁移

```bash
alembic upgrade head
```

该命令会创建本地 SQLite 数据库以及项目所需的数据表。

### 5. 启动 API 服务

```bash
uvicorn app.main:app --reload
```

API 地址：

```text
http://127.0.0.1:8000
```

交互式 API 文档地址：

```text
http://127.0.0.1:8000/docs
```

## API 接口

| 请求方法 | 接口 | 说明 |
| --- | --- | --- |
| `GET` | `/` | 检查 API 是否正常运行 |
| `POST` | `/prompts` | 创建提示词 |
| `GET` | `/prompts` | 获取提示词列表 |
| `GET` | `/prompts?tag={tag}` | 根据标签筛选提示词 |
| `GET` | `/prompts/search?q={query}` | 搜索提示词 |
| `GET` | `/prompts/{prompt_id}` | 获取指定提示词 |
| `PUT` | `/prompts/{prompt_id}` | 更新指定提示词 |
| `DELETE` | `/prompts/{prompt_id}` | 删除指定提示词 |

## 请求示例

创建一个提示词：

```bash
curl -X POST http://127.0.0.1:8000/prompts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Code Review",
    "content": "Review the following code and identify potential problems.",
    "tags": ["development", "review"]
  }'
```

响应示例：

```json
{
  "id": 1,
  "title": "Code Review",
  "content": "Review the following code and identify potential problems.",
  "tags": [
    "development",
    "review"
  ],
  "created_at": "2026-07-26T12:00:00",
  "updated_at": "2026-07-26T12:00:00"
}
```

## 数据库迁移

执行全部迁移：

```bash
alembic upgrade head
```

查看当前迁移版本：

```bash
alembic current
```

回滚全部迁移：

```bash
alembic downgrade base
```

重新执行全部迁移：

```bash
alembic upgrade head
```

## 测试与代码检查

运行完整测试：

```bash
python -m pytest -q
```

运行 Ruff 代码质量检查：

```bash
ruff check app tests migrations
```

检查空白字符错误：

```bash
git diff --check
```

## Docker

### 构建镜像

```bash
docker build -t prompt-vault-api .
```

### 启动容器

```bash
docker run --rm \
  --name prompt-vault-api \
  -p 8000:8000 \
  prompt-vault-api
```

容器会在启动 API 服务之前自动执行最新的 Alembic 数据库迁移。

## Docker Compose

构建并启动服务：

```bash
docker compose up --build
```

在后台启动服务：

```bash
docker compose up -d --build
```

查看服务状态：

```bash
docker compose ps
```

停止并删除服务：

```bash
docker compose down
```

## 持续集成

GitHub Actions 工作流会在代码推送和 Pull Request 创建时自动运行。

CI 工作流会执行以下检查：

1. 配置 Python 3.12
2. 安装项目及开发依赖
3. 运行 Ruff
4. 运行 pytest 测试
5. 验证 Alembic 数据库升级和回滚

## 当前项目范围

当前版本暂不包含以下功能：

- 用户身份认证
- 权限控制
- 前端界面
- 云端部署
- 多种数据库后端

这些功能不属于本项目的初始需求范围。
