import os
import textwrap

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, filters

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("未在 .env 中找到 BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 获取用户的名字
    first_name = update.effective_user.first_name
    user_id = update.effective_user.id
    bot_username = context.bot.username

    # 定义内联按钮
    inline_keyboard = [
        [InlineKeyboardButton('➕把我加到群组➕', url=f"https://t.me/{bot_username}?startgroup=addbot")]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)

    # 使用 MarkdownV2 格式定义消息文本
    message_text = textwrap.dedent(f"""\
    嗨，*[{first_name}](tg://user?id={user_id})*！
    [TG Helper](https://t.me/dsafsad21) 能帮助你方便地 *安全管理* 你的群组，是 TG 上 *最完美* 的机器人！

    将我添加到群组并授予管理员权限，这样我才能进行操作！
    点击 /help 查看所有指令及使用方法。
    """)

    await update.message.reply_markdown_v2(
        message_text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    # 弹出提示窗口，显示"添加到群组"
    await query.answer("添加到群组", show_alert=True)


async def on_my_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    old_status = update.chat_member.old_chat_member.status
    new_status = update.chat_member.new_chat_member.status

    # 当状态从 'left'/'kicked' 变成 'member'/'administrator' 时，说明机器人被添加进群
    if old_status in ['left', 'kicked'] and new_status in ['member', 'administrator']:
        chat_id = update.chat_member.chat.id
        await context.bot.send_message(
            chat_id=chat_id,
            text="感谢您将我添加到群组！"
        )

async def handle_start_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.edit_text("这是专门响应 /start@krinxbot 命令的回复！")

if __name__ == '__main__':
    # 构建 Application 实例，并添加命令处理器
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start, filters=filters.ChatType.PRIVATE))
    app.add_handler(CallbackQueryHandler(button_callback))
    # app.add_handler(ChatMemberHandler(on_my_chat_member))
    # 使用正则表达式过滤器匹配以 /start@krinxbot 开头的命令
    mention_filter = filters.Regex(r'^/start@krinxbot\b')
    app.add_handler(CommandHandler("start", handle_start_mention, filters=mention_filter))


    # 运行机器人（采用异步轮询）
    app.run_polling()
