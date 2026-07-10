# 微信聊天记录分析 Skill 使用指南

## 技能简介

这是一个 Claude Code Skill，可以分析本地微信聊天记录，并结合阿里云百炼大模型进行深度分析。

## 前置要求

### 1. 安装 wechat-cli

```bash
# 需要 Python 环境
pip install wechat-chat-export

# 初始化配置（首次使用）
wechat-cli init
# 按提示操作：启动微信PC版 → 扫描二维码 → 允许访问
```

### 2. 安装百炼 CLI (bl)

```bash
# 需要 Node.js 环境
npm install -g @ali/bailian-cli

# 配置 API 密钥
bl configure
# 从 https://bailian.console.aliyun.com/ 获取 API Key
```

### 3. 配置 Claude Code 权限

在 Claude Code 中执行：
```
/update-config
```

添加两条权限：
- `wechat-cli *` - 读取微信数据
- `bl *` - 调用百炼模型

## 使用方法

### 触发方式

直接在对话中描述需求，技能会自动触发。

### 基础分析（本地统计）

**触发示例**：
- "分析微信聊天记录"
- "查看XX群的消息"
- "这个群谁最活跃"
- "统计聊天数据"

**执行流程**：
1. `wechat-cli sessions` - 获取会话列表
2. `wechat-cli history "群名" --days 7 --format json` - 获取聊天记录
3. 本地统计：活跃用户、消息数量、高峰时段、话题分布
4. 输出分析报告

### 深度分析（百炼模型）

**触发示例**：
- "用AI深度分析XX群"
- "让百炼分析这段聊天"
- "智能分析投资群"

**执行流程**：
1. `wechat-cli history` - 获取聊天记录
2. `bl generate --model qwen-max --prompt "分析以下对话..."` - 调用百炼
3. 整合输出深度报告

### 指定群名称

**示例**：
- "分析"技术讨论群"的聊天记录"
- "查看"投资交流群"谁最活跃"

## 常见问题

### 微信数据未找到
```bash
# 确认微信PC版已启动
open /Applications/WeChat.app

# 重新初始化
wechat-cli init

# 查看可用群列表
wechat-cli sessions --limit 20
```

### 百炼API调用失败
```bash
# 重新配置
bl configure

# 验证
bl list-models
```

### 权限被拒绝
```
/update-config
```
添加 `wechat-cli *` 和 `bl *` 权限

## 安全说明

- 所有分析在本地执行
- 聊天记录不会上传到任何服务器
- 百炼API仅发送脱敏后的内容片段
