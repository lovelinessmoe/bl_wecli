---
name: wechat-chat-analyzer
description: 分析微信聊天记录、查询群聊消息、查看用户活跃度、调用百炼模型深度分析
---

# wechat-chat-analyzer

微信聊天记录智能分析专家

## 触发条件

当用户请求以下操作时自动触发：

- 分析微信聊天记录
- 查询群聊消息历史
- 查看某个群/联系人的活跃度
- 用百炼模型分析聊天内容
- `/analyze-chat` 命令
- `/wechat` 相关命令

## 使用方法

### 基础分析（本地统计）

当用户说类似以下内容时：

- "分析微信聊天记录"
- "查看XX群的消息"
- "这个群谁最活跃"
- "统计聊天数据"

执行本地分析命令，无需调用百炼API：

1. 使用 `wechat-cli sessions` 获取会话列表
2. 使用 `wechat-cli history "群名" --days 7 --format json` 获取聊天记录
3. 解析消息进行统计分析（活跃用户、消息数量、高峰时段等）
4. 生成结构化报告

### 深度分析（百炼模型）

当用户说以下内容时：

- "深度分析"
- "用AI分析"
- "百炼分析"
- `--depth=high`

执行以下步骤：

1. 使用 `wechat-cli history` 获取聊天记录
2. 调用 `bl generate --model qwen-max --prompt "分析以下对话..."` 获取AI分析
3. 整合本地统计和AI分析结果

## 示例

### 示例1：分析最近7天聊天记录

```
用户：分析一下"技术讨论群"的聊天记录
→ 执行：wechat-cli history "技术讨论群" --days 7 --format json
→ 统计活跃用户、消息数量、话题分布
→ 输出分析报告
```

### 示例2：百炼深度分析

```
用户：用AI深度分析"投资群"
→ 执行：wechat-cli history "投资群" --days 7
→ 调用 bl generate --model qwen-max
→ 输出深度分析报告
```

## 注意事项

- 使用 `wechat-cli` 前需确保微信PC版已登录
- 百炼分析需要先运行 `bl configure` 配置API
- 所有分析均在本地执行，聊天记录不会上传
