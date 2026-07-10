# bl_wecli：微信聊天记录分析专家

[![技能状态](https://img.shields.io/badge/status-verified-green)](https://github.com/lovelinessmoe/bl_wecli)
[![依赖状态](https://img.shields.io/badge/dependencies-wechat--cli%20%7C%20bl-blue)](https://github.com/TKsW/wechat-chat-export)

> 📱 结合本地微信数据与阿里云百炼大模型的智能聊天分析技能
> 
> **一句话说明**：通过 `/analyze-chat "群名称"` 命令，自动获取7天内聊天记录，调用百炼模型生成深度分析报告

## 🔍 核心能力

| 分析维度       | 说明                                                                 | 示例命令                                  |
|----------------|----------------------------------------------------------------------|-------------------------------------------|
| **基础统计**   | 消息数量、活跃时段、高频用户                                         | `/analyze-chat "AI群"`                  |
| **深度语义**   | 话题聚类、情感分析、决策模式识别（调用百炼qwen-max模型）             | `/analyze-chat "投资群" --depth=high`   |
| **上下文洞察** | 结合发言前后消息分析意图，识别关键决策点                             | `/analyze-chat "项目群" --aspect=决策` |

## ⚙️ 安装指南

### 前置条件
1. 安装微信聊天导出工具：[wechat-cli](https://github.com/TKsW/wechat-chat-export)（需微信PC版）
   ```bash
   pip install wechat-chat-export
   wechat-cli init
   ```
2. 配置百炼CLI（阿里云）：
   ```bash
   bl configure
   # 按提示输入AccessKey（需开通百炼服务）
   ```

### 技能安装（Claude Code）
```bash
# 1. 注册技能
/skills-manager
install lovelinessmoe/bl_wecli

# 2. 授权必要权限
/update-config
allow wechat-cli *
allow bl *
```

> 💡 **权限说明**：技能仅访问您本地的微信数据，**不会**上传聊天记录到任何服务器

## 🚀 使用示例

### 基础分析（7天内记录）
```bash
/analyze-chat "技术讨论群"
```
**输出示例**：
```
📊 基础分析报告
• 总消息数：248条
• 活跃用户：12人（@张三、@李四等）
• 高峰时段：工作日10:00-12:00
• 热门话题：LLM应用（23%）、工具分享（18%）
```

### 深度模型分析
```bash
/analyze-chat "投资交流群" --depth=high --aspect=风险评估
```
**执行流程**：
1. 通过 `wechat-cli` 获取原始聊天记录
2. 提取关键对话片段
3. 调用 `bl generate --model qwen-max` 生成专业分析
4. 整合输出结构化报告

## 🔐 安全说明

- 所有微信数据均**本地处理**，不会上传任何服务
- 百炼API调用仅发送**脱敏后的内容片段**（截取关键5000字符）
- 完整权限控制：
  ```json
  // .claude/settings.json
  {
    "permissions": {
      "bash": [
        {
          "command": "wechat-cli *",
          "description": "仅读取本地微信数据"
        },
        {
          "command": "bl *",
          "description": "调用阿里云百炼服务分析"
        }
      ]
    }
  }
  ```

## 🌟 贡献指南

欢迎提交PR改进：
1. 增加分析维度（如：`--aspect=冲突检测`）
2. 优化百炼提示词模板（`references/prompt_templates/`）
3. 补充多语言支持

```bash
# 本地开发流程
git clone https://github.com/lovelinessmoe/bl_wecli.git
/skills-manager register ./bl_wecli
```

---

> MIT License © 2026 lovelinessmoe | 基于 [Claude Code Skills](https://docs.anthropic.com/claude-code/skills) 构建