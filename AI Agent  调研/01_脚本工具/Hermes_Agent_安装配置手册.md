# Hermes Agent 安装配置手册

> 本文档记录了完整的安装和配置过程，可用于在其他电脑上快速复制部署。
> 最后更新：2026-04-14
> 运行环境：macOS (Apple Silicon)

---

## 一、前置要求

- macOS (Apple Silicon 或 Intel)
- 16GB+ 内存
- Homebrew 已安装
- Node.js 已安装
- 网络能访问 GitHub 和 PyPI（国内需要镜像）

---

## 二、安装步骤

### 2.1 安装 Ollama（本地模型运行时）

```bash
brew install ollama
```

### 2.2 安装 uv（Python 包管理）

```bash
brew install uv
```

### 2.3 下载 Hermes Agent

```bash
mkdir -p ~/.hermes
git clone --depth 1 https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent
```

### 2.4 创建虚拟环境并安装依赖

```bash
cd ~/.hermes/hermes-agent
uv venv .venv --python 3.11
# 使用清华镜像源（国内加速）
uv pip install -e . --python .venv/bin/python --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2.5 安装飞书 SDK

```bash
uv pip install lark-oapi --python ~/.hermes/hermes-agent/.venv/bin/python --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2.6 验证安装

```bash
cd ~/.hermes/hermes-agent && .venv/bin/python hermes --version
# 应输出: Hermes Agent v0.8.0 (2026.4.8)
```

---

## 三、下载本地模型（可选）

如果需要本地模型（免费但 Agent 能力弱），从国内镜像下载：

```bash
# 启动 Ollama
ollama serve &

# 从 ModelScope 国内镜像下载 Hermes 3 8B（约 4.9GB）
ollama run modelscope.cn/XD_AI/Hermes-3-Llama-3.1-8B-GGUF:Q4_K_M --keepalive 0 "" 
```

---

## 四、配置文件

### 4.1 主配置文件 `~/.hermes/config.yaml`

**使用 DeepSeek API（推荐）：**

```yaml
model:
  default: "deepseek-chat"
  provider: "custom"
  base_url: "https://api.deepseek.com/v1"
  api_key: "你的DeepSeek API Key"
```

**使用本地 Ollama 模型（备选）：**

```yaml
model:
  default: "modelscope.cn/XD_AI/Hermes-3-Llama-3.1-8B-GGUF:Q4_K_M"
  provider: "custom"
  base_url: "http://localhost:11434/v1"
  api_key: "no-key-required"
```

**使用 OpenRouter（多模型）：**

```yaml
model:
  default: "anthropic/claude-sonnet-4"
  provider: "openrouter"
```

### 4.2 环境变量 `~/.hermes/.env`

```bash
# DeepSeek API
OPENAI_API_KEY=你的DeepSeek API Key
OPENAI_BASE_URL=https://api.deepseek.com/v1

# 飞书机器人配置
FEISHU_APP_ID=cli_a9572f59a3f81bd2
FEISHU_APP_SECRET=JJlj8YYRHVdekWsPpuQJbcHY5hBMDLGX
FEISHU_DOMAIN=feishu
FEISHU_CONNECTION_MODE=websocket
GATEWAY_ALLOW_ALL_USERS=true
```

### 4.3 认证缓存 `~/.hermes/auth.json`

如果出现 503 或连接旧端点的问题，清空此文件：

```json
{
  "version": 1,
  "providers": {},
  "credential_pool": {},
  "updated_at": "2026-04-14T00:00:00.000000+00:00"
}
```

---

## 五、飞书机器人配置

### 5.1 飞书开放平台设置

1. 访问 https://open.feishu.cn/app
2. 创建企业自建应用
3. 添加 **机器人** 能力
4. 开通权限（批量导入 JSON）：

```json
[
  {"name": "im:message"},
  {"name": "im:message:send_as_bot"},
  {"name": "im:chat:readonly"},
  {"name": "im:resource"},
  {"name": "sheets:spreadsheet:readonly"},
  {"name": "docs:doc:readonly"},
  {"name": "drive:drive:readonly"},
  {"name": "bitable:bitable:readonly"},
  {"name": "bitable:app:readonly"},
  {"name": "bitable:app"},
  {"name": "wiki:wiki:readonly"},
  {"name": "contact:user.id:readonly"},
  {"name": "contact:user.base:readonly"},
  {"name": "admin:app.info:readonly"},
  {"name": "application:application:self_manage"}
]
```

5. 事件与回调 → 订阅方式选 **WebSocket** → 添加事件 `im.message.receive_v1`
6. 发布版本

### 5.2 启动飞书网关

```bash
cd ~/.hermes/hermes-agent && .venv/bin/python hermes gateway start
```

---

## 六、Open WebUI 安装（网页聊天界面）

```bash
pip3 install open-webui

# 启动（连接本地 Ollama）
RAG_EMBEDDING_ENGINE="" RAG_EMBEDDING_MODEL="" \
OLLAMA_BASE_URL=http://localhost:11434 \
/path/to/open-webui serve --port 8080 &
```

> open-webui 二进制路径可能是 `/Users/用户名/Library/Python/3.12/bin/open-webui`

浏览器访问 http://localhost:8080

---

## 七、一键启动脚本

保存为 `~/.hermes/start.sh`：

```bash
#!/bin/bash
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
mkdir -p ~/.hermes/logs

# 启动 Ollama
OLLAMA_KEEP_ALIVE="-1" ollama serve &>/dev/null &
sleep 2

# 启动 Open WebUI
RAG_EMBEDDING_ENGINE="" RAG_EMBEDDING_MODEL="" \
OLLAMA_BASE_URL=http://localhost:11434 \
/Users/用户名/Library/Python/3.12/bin/open-webui serve --port 8080 &>/dev/null &

# 启动飞书网关
cd ~/.hermes/hermes-agent && .venv/bin/python hermes gateway start &>/dev/null
```

```bash
chmod +x ~/.hermes/start.sh
# 添加快捷命令
echo 'alias hermes-start="bash ~/.hermes/start.sh"' >> ~/.zshrc
```

---

## 八、开机自动启动

保存为 `~/Library/LaunchAgents/com.hermes.autostart.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hermes.autostart</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/用户名/.hermes/start.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardOutPath</key>
    <string>/Users/用户名/.hermes/logs/autostart.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/用户名/.hermes/logs/autostart.error.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
```

```bash
# 注册开机启动
launchctl load ~/Library/LaunchAgents/com.hermes.autostart.plist
```

---

## 九、常用命令

| 命令 | 说明 |
|------|------|
| `hermes-start` | 一键启动所有服务 |
| `cd ~/.hermes/hermes-agent && .venv/bin/python hermes` | 进入 CLI 对话 |
| `cd ~/.hermes/hermes-agent && .venv/bin/python hermes gateway start` | 启动飞书网关 |
| `cd ~/.hermes/hermes-agent && .venv/bin/python hermes gateway restart` | 重启飞书网关 |
| `cd ~/.hermes/hermes-agent && .venv/bin/python hermes gateway stop` | 停止飞书网关 |
| `cd ~/.hermes/hermes-agent && .venv/bin/python hermes --version` | 查看版本 |
| `ollama ps` | 查看已加载的模型 |
| `ollama list` | 查看已下载的模型 |

---

## 十、常见问题

### Q: 飞书机器人报 503 错误
- 检查 DeepSeek API Key 余额：https://platform.deepseek.com
- 检查 `~/.hermes/config.yaml` 的 base_url 是否正确
- 清空 `~/.hermes/auth.json` 的 credential_pool 后重启网关

### Q: 飞书机器人没反应
- 检查网关是否运行：`ps aux | grep "hermes gateway"`
- 查看日志：`tail -20 ~/.hermes/logs/gateway.error.log`
- 重启网关

### Q: 本地模型 Ollama 503
- 检查模型是否加载：`ollama ps`
- 手动加载：`curl -s http://localhost:11434/api/generate -d '{"model":"模型名","prompt":"hi","stream":false}'`
- 设置永不卸载：`export OLLAMA_KEEP_ALIVE="-1"`

### Q: 权限不足（飞书）
- 去飞书开放平台添加对应权限
- 重新发布版本
- 重启网关

---

## 十一、DeepSeek API 注册

1. 访问 https://platform.deepseek.com
2. 手机号注册
3. 左侧菜单 → API Keys → 创建 API Key
4. 充值 → 最低 10 元
5. 将 Key 填入 `~/.hermes/config.yaml` 和 `~/.hermes/.env`

---

## 十二、飞书多维表格读写

### 12.1 安装脚本

将以下两个脚本放到 `~/.hermes/scripts/` 目录：
- `feishu_bitable.py` — 多维表格（Bitable）读写
- `feishu_sheets.py` — 普通电子表格读写

### 12.2 使用方法

```bash
# 查看所有数据表
python3 ~/.hermes/scripts/feishu_bitable.py tables "飞书表格URL"

# 读取多维表格数据
python3 ~/.hermes/scripts/feishu_bitable.py read "飞书表格URL"

# 写入数据
python3 ~/.hermes/scripts/feishu_bitable.py write "飞书表格URL" '[{"字段名":"值"}]'
```

### 12.3 在飞书机器人中使用

Hermes Agent 默认会用浏览器访问飞书链接（会失败，因为需要登录）。正确的方式是让它用 API。

**发给飞书机器人的提示模板：**

```
不要用浏览器访问链接。用飞书开放平台 API 读取这个多维表格。
App ID: cli_a9572f59a3f81bd2
App Secret: 你的App Secret
多维表格 app_token: 从URL中提取
数据表 table_id: 从URL中提取

先用 tenant_access_token 获取令牌，再调用 bitable API 读取记录。
```

或者直接让机器人执行脚本：

```
请执行这个命令来读取表格：
python3 ~/.hermes/scripts/feishu_bitable.py read "飞书表格URL"
```

### 12.4 URL 解析说明

飞书多维表格 URL 格式：
```
https://xxx.feishu.cn/base/{app_token}?table={table_id}&view={view_id}
```

例如：
```
https://w5scrwkn9y.feishu.cn/base/CuiybJoOMafb9HsZbu2cfVhfnZg?table=tblLIHsNVlhfCEer&view=vewKkig5fe
```
- app_token = `CuiybJoOMafb9HsZbu2cfVhfnZg`
- table_id = `tblLIHsNVlhfCEer`
- view_id = `vewKkig5fe`

### 12.5 API 调用原理

脚本的工作流程：

```
1. 用 App ID + App Secret 获取 tenant_access_token
   POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal

2. 用 token 列出数据表
   GET https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables

3. 获取字段定义
   GET https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields

4. 读取记录
   GET https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records

5. 写入记录
   POST https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create

6. 更新记录
   PUT https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}
```

### 12.6 必需的飞书权限

多维表格操作需要以下权限（在飞书开放平台 → 权限管理中开通）：

| 权限 | 说明 |
|------|------|
| `bitable:app:readonly` | 查看多维表格 |
| `bitable:app` | 读写多维表格 |
| `base:table:read` | 读取数据表 |

开通权限后必须**重新发布版本**才生效。

### 12.7 注意事项

- 机器人只能访问**已共享给它的表格**，或者**应用有对应权限的表格**
- 如果表格在某个文件夹中，可能还需要 `drive:drive:readonly` 权限
- 每次修改权限后都需要在飞书开放平台**重新发布版本**

---

> **给 Claude Code 的指令：** 如果用户提供此文档并要求配置新电脑，请按照以上步骤依次执行。需要用户提供的信息：DeepSeek API Key、飞书 App ID 和 App Secret。其他步骤均可自动完成。
