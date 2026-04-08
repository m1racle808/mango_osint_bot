from telegram import Update
from telegram.ext import ContextTypes
from config import CHANNEL_ID, CHANNEL_LINK
from keyboards import check_subscription_button

async def check_subscription(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Проверяет, подписан ли пользователь на канал"""
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def require_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Декоратор-проверка подписки. Возвращает True если подписан"""
    user_id = update.effective_user.id
    
    if await check_subscription(user_id, context):
        return True
    
    # Не подписан - просим подписаться
    await update.message.reply_text(
        f"❌ Для использования бота необходимо подписаться на наш канал!\n\n"
        f"👉 {CHANNEL_LINK}\n\n"
        f"После подписки нажмите кнопку ниже:",
        reply_markup=check_subscription_button()
    )
    return False
