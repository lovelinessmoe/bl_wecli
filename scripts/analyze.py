#!/usr/bin/env python3
"""
微信聊天记录智能分析工具
功能：整合微信数据与百炼大模型生成深度洞察
版本：1.2.0
"""
import sys
import json
import subprocess
import datetime
import re
import argparse
import logging
from typing import Dict, List, Optional, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)

class WeChatAnalyzer:
    """微信聊天记录分析核心类"""

    ERROR_CODES = {
        "E001": "微信数据未找到 - 请确认微信PC版已登录且群名称正确",
        "E002": "百炼API调用失败 - 请检查bl configure配置",
        "E003": "权限拒绝 - 请通过/update-config授权",
        "E004": "时间格式错误 - 请使用YYYY-MM-DD格式"
    }

    def __init__(self):
        self.chat_history = []
        self.stats = {
            "total_messages": 0,
            "active_users": {},
            "time_distribution": {},
            "topic_frequency": {}
        }

    def get_wechat_history(self, chat_name: str, start: datetime.datetime, end: datetime.datetime) -> Dict:
        """获取微信聊天记录（支持分页）"""
        all_messages = []
        offset = 0
        limit = 500  # 每页消息数

        while True:
            try:
                cmd = [
                    "wechat-cli", "history", chat_name,
                    "--start-time", start.strftime("%Y-%m-%d"),
                    "--end-time", end.strftime("%Y-%m-%d %H:%M:%S"),
                    "--limit", str(limit),
                    "--offset", str(offset),
                    "--format", "json"
                ]

                logging.info(f"执行命令: {' '.join(cmd)}")
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True
                )

                data = json.loads(result.stdout)
                messages = data.get("messages", [])
                all_messages.extend(messages)

                # 检查是否还有更多消息
                if len(messages) < limit:
                    break

                offset += limit

            except subprocess.CalledProcessError as e:
                if "No chat found" in e.stderr:
                    raise RuntimeError(self.ERROR_CODES["E001"]) from None
                logging.error(f"wechat-cli 错误: {e.stderr}")
                raise

            except json.JSONDecodeError:
                raise RuntimeError("微信数据解析失败 - 请检查wechat-cli版本") from None

        return {"messages": all_messages}

    def analyze_locally(self, messages: List[Dict]) -> Dict:
        """本地分析（无需百炼API）"""
        stats = {
            "total_messages": len(messages),
            "active_users": {},
            "hourly_activity": [0] * 24,
            "topic_keywords": {}
        }

        # 提取活跃用户
        for msg in messages:
            sender = msg.get("sender", "未知用户")
            stats["active_users"][sender] = stats["active_users"].get(sender, 0) + 1

            # 提取时间分布
            try:
                hour = int(msg["timestamp"].split()[1].split(":")[0])
                stats["hourly_activity"][hour] += 1
            except (KeyError, ValueError, IndexError):
                pass

            # 提取关键词
            content = msg.get("content", "").lower()
            for word in ["llm", "模型", "api", "部署", "优化"]:
                if word in content:
                    stats["topic_keywords"][word] = stats["topic_keywords"].get(word, 0) + 1

        # 计算峰值时段
        peak_hour = stats["hourly_activity"].index(max(stats["hourly_activity"]))

        return {
            **stats,
            "peak_time": f"{peak_hour:02d}:00-{(peak_hour+1):02d}:00",
            "top_topics": sorted(
                stats["topic_keywords"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
        }

    def analyze_with_bl(self, messages: List[Dict], aspect: str) -> str:
        """调用百炼大模型进行深度分析"""
        if not messages:
            return "无消息可供分析"

        # 提取最近50条消息用于分析（避免超出token限制）
        context = "\n".join([
            f"{msg['sender']}: {msg['content']}"
            for msg in messages[-50:]
        ])

        # 构建提示词
        prompt = f"""作为专业聊天分析师，请对以下{aspect}进行深度分析：

【分析要求】
1. 识别核心讨论议题及演变过程
2. 分析参与者立场和决策模式
3. 指出潜在风险或机会点
4. 用具体消息片段作为证据

【聊天片段】
{context[:5000]}

【输出要求】
- 使用中文输出
- 包含具体时间戳引用
- 按议题分类呈现
- 避免笼统描述，给出可执行建议"""

        try:
            cmd = [
                "bl", "generate",
                "--model", "qwen-max",
                "--prompt", prompt
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout

        except subprocess.CalledProcessError as e:
            logging.error(f"百炼API错误: {e.stderr}")
            raise RuntimeError(self.ERROR_CODES["E002"]) from None

    def generate_report(self, chat_name: str, stats: Dict, bl_analysis: Optional[str] = None) -> str:
        """生成结构化报告"""
        report = f"# {chat_name} 聊天分析报告\n\n"

        # 基础统计
        report += "## 基础统计\n"
        report += f"- 消息总数: {stats['total_messages']} 条\n"
        report += f"- 活跃用户: {len(stats['active_users'])} 人\n"

        # 顶部活跃用户
        top_users = sorted(
            stats['active_users'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        report += "- 最活跃用户: " + ", ".join([f"@{u} ({c}条)" for u, c in top_users]) + "\n"

        report += f"- 高峰时段: {stats['peak_time']}\n"
        report += "- 热门话题: " + ", ".join([f"{k} ({v}次)" for k, v in stats['top_topics']]) + "\n\n"

        # 百炼分析
        if bl_analysis:
            report += "## 百炼深度分析\n"
            report += bl_analysis

        # 安全声明
        report += "\n\n---\n> 本报告由本地分析生成，聊天记录未上传任何服务器"

        return report

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="微信聊天记录分析工具")
    parser.add_argument("chat_name", help="微信群/联系人名称")

    # 分析参数
    parser.add_argument("--depth", choices=["standard", "high"], default="standard", help="分析深度")
    parser.add_argument("--aspect", default="全面分析", help="分析维度")

    # 过滤参数
    parser.add_argument("--search", help="关键词搜索")
    parser.add_argument("--user", help="指定分析用户")

    # 时间参数
    parser.add_argument("--start", help="开始时间 (YYYY-MM-DD)")
    parser.add_argument("--end", help="结束时间 (YYYY-MM-DD)")

    return parser.parse_args()

def main():
    try:
        args = parse_args()
        analyzer = WeChatAnalyzer()

        # 设置时间范围（默认7天）
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(days=7)

        if args.start:
            try:
                start_time = datetime.datetime.strptime(args.start, "%Y-%m-%d")
            except ValueError:
                raise RuntimeError(analyzer.ERROR_CODES["E004"]) from None

        if args.end:
            try:
                end_time = datetime.datetime.strptime(args.end, "%Y-%m-%d")
            except ValueError:
                raise RuntimeError(analyzer.ERROR_CODES["E004"]) from None

        # 获取聊天记录
        logging.info(f"正在获取 {args.chat_name} 的聊天记录...")
        history = analyzer.get_wechat_history(args.chat_name, start_time, end_time)

        # 执行基础分析
        logging.info("正在执行本地统计分析...")
        stats = analyzer.analyze_locally(history["messages"])

        # 执行深度分析（如需）
        bl_analysis = None
        if args.depth == "high":
            logging.info(f"正在调用百炼进行 {args.aspect}...")
            bl_analysis = analyzer.analyze_with_bl(history["messages"], args.aspect)

        # 生成报告
        report = analyzer.generate_report(args.chat_name, stats, bl_analysis)
        print(report)

    except RuntimeError as e:
        error_code = next((k for k, v in WeChatAnalyzer.ERROR_CODES.items() if v == str(e)), None)
        if error_code:
            print(f"[{error_code}] {e}")
            sys.exit(1)
        else:
            print(f"未知错误: {e}")
            sys.exit(1)
    except Exception as e:
        logging.exception("意外错误发生")
        print(f"系统错误: {str(e)[:200]}...")
        sys.exit(1)

if __name__ == "__main__":
    main()
