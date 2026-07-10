# 故障排除指南

## 常见错误解决方案

### E001: 微信数据未找到

**原因**：
- 微信PC版未登录或未运行
- 群名称与`wechat-cli sessions`输出不匹配
- wechat-cli未正确初始化

**解决步骤**：
```bash
# 1. 确认微信PC版已启动
open /Applications/WeChat.app

# 2. 重新初始化wechat-cli
wechat-cli init

# 3. 确认群名称
wechat-cli sessions --limit 20
```

### E002: 百炼API调用失败

**原因**：
- 百炼CLI未配置
- 阿里云AccessKey过期
- 百炼服务未开通

**解决步骤**：
```bash
# 1. 配置百炼CLI
bl configure

# 2. 验证配置
bl list-models

# 3. 确认服务开通
open https://bailian.console.aliyun.com/
```

### E003: 权限拒绝

**原因**：未通过`/update-config`授权

**解决步骤**：
1. 在Claude Code中输入：`/update-config`
2. 在打开的配置界面：
   - 选择 "Bash 权限" 选项卡
   - 点击 "添加新权限"
   - 输入：`wechat-cli *` 和 `bl *`
3. 点击 "保存"

### E004: 时间格式错误

**原因**：使用了错误的时间格式

**解决**：使用 `YYYY-MM-DD` 格式，例如：`--start 2024-07-01`

---

## 高级调试

### 检查技能执行日志
```bash
# 测试微信数据获取
wechat-cli history "测试群" --limit 10 --format json

# 测试百炼调用
bl generate --model qwen-max --prompt "分析: 测试"
```

---

> 所有操作均在本地执行，聊天记录不会上传任何服务器
