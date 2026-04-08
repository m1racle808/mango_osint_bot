from telegram import Update
from telegram.ext import ContextTypes
from keyboards import main_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_text = (
        "🍋 <b>Mango Instruments - OSINT</b>\n\n"
        "Профессиональный OSINT-инструмент для расследований.\n\n"
        "Возможности:\n"
        "📊 <b>OSINT-отчёт</b> - генерация детального отчёта по личности/компании/проекту\n"
        "🔗 <b>Логическая цепочка</b> - построение ветвящейся схемы расследования\n\n"
        "Все данные генерируются в формате PDF.\n\n"
        "Выберите действие в меню ниже:"
    )
    await update.message.reply_text(welcome_text, parse_mode='HTML', reply_markup=main_menu())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопки Помощь"""
    help_text = (
        "📖 <b>Инструкция по использованию</b>\n\n"
        "<b>OSINT-отчёт:</b>\n"
        "1. Нажмите на кнопку\n"
        "2. Выберите тип (личность/компания/проект)\n"
        "3. Отвечайте на вопросы бота\n"
        "4. Получите PDF-отчёт\n\n"
        "<b>Логическая цепочка:</b>\n"
        "1. Нажмите на кнопку\n"
        "2. Введите email, телефон или username\n"
        "3. Выбирайте дальнейшие действия из предложенных\n"
        "4. В конце получите PDF со схемой\n\n"
        "<b>В любой момент можно нажать ❌ Отмена</b>"
    )
    await update.message.reply_text(help_text, parse_mode='HTML', reply_markup=main_menu())
