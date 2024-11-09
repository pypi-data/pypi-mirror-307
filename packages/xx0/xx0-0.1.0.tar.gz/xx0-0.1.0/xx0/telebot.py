# 导入所需的库
import telebot
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 使用环境变量中的token初始化机器人
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

# 处理 /start 命令
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "你好! 我是你的个人助理机器人。\n"
                         "使用 /help 查看所有可用命令。")

# 处理 /help 命令
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
可用命令列表:
/start - 开始使用机器人
/help - 显示此帮助信息
/todo - 显示待办事项列表
/add <任务名称> - 添加新的待办事项
/complete <任务ID> - 完成待办事项
"""
    bot.reply_to(message, help_text)

# 处理 /todo 命令
# 显示所有待办事项
@bot.message_handler(commands=['todo'])
def show_todos(message):
    # TODO: 实现待办事项列表功能
    bot.reply_to(message, "待办事项功能正在开发中...")

# 处理 /add 命令
@bot.message_handler(commands=['add'])
def add_todo(message):
    # TODO: 实现添加待办事项功能
    bot.reply_to(message, "添加待办事项功能正在开发中...")

# 处理 /complete 命令
@bot.message_handler(commands=['complete'])
def complete_todo(message):
    # TODO: 实现完成待办事项功能
    bot.reply_to(message, "完成待办事项功能正在开发中...")

# 处理所有其他消息
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "抱歉，我不明白这个命令。使用 /help 查看所有可用命令。")

# 启动机器人
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()