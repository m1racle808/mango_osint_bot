from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from keyboards import report_type_buttons, main_menu
from states import *
from pdf_generator import PDFGenerator
from subscription import require_subscription
import states

async def report_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало создания отчёта"""
    if not await require_subscription(update, context):
        return ConversationHandler.END
    
    await update.message.reply_text(
        "📊 Выберите тип OSINT-отчёта:",
        reply_markup=report_type_buttons()
    )
    return states.REPORT_TYPE

async def report_type_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка выбора типа отчёта"""
    query = update.callback_query
    await query.answer()
    
    choice = query.data
    if choice == "report_person":
        context.user_data['report_type'] = 'person'
        await query.edit_message_text("👤 Введите ФИО личности:")
        return states.REPORT_PERSON_NAME
    elif choice == "report_company":
        context.user_data['report_type'] = 'company'
        await query.edit_message_text("🏢 Введите название компании:")
        return states.REPORT_COMPANY_NAME
    elif choice == "report_project":
        context.user_data['report_type'] = 'project'
        await query.edit_message_text("📁 Введите название проекта:")
        return states.REPORT_PROJECT_NAME
    elif choice == "cancel":
        await query.edit_message_text("❌ Отменено.", reply_markup=main_menu())
        return ConversationHandler.END

async def get_person_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['person_name'] = update.message.text
    await update.message.reply_text("📝 Введите никнейм (или '-' если нет):")
    return states.REPORT_PERSON_NICK

async def get_person_nick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['person_nick'] = update.message.text if update.message.text != '-' else 'Не указан'
    await update.message.reply_text("🏙️ Введите город (или '-' если нет):")
    return states.REPORT_PERSON_CITY

async def get_person_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['person_city'] = update.message.text if update.message.text != '-' else 'Не указан'
    
    # Генерация демо-данных для отчёта
    report_data = {
        'input': {
            'ФИО': context.user_data['person_name'],
            'Никнейм': context.user_data['person_nick'],
            'Город': context.user_data['person_city']
        },
        'findings': {
            'Социальные сети': ['Telegram: @' + context.user_data['person_nick'].replace(' ', '_'), 
                               'VK: vk.com/id123456'],
            'Email-адреса': [f"{context.user_data['person_name'].split()[0].lower()}.@mail.ru"],
            'Активность': 'Найден в 5 публичных чатах, посты на тему IT'
        },
        'risks': [
            'Публичные данные о месте работы',
            'Активное присутствие в соцсетях',
            'Использование одинакового никнейма на разных платформах'
        ],
        'recommendations': [
            'Проверить настройки приватности в соцсетях',
            'Использовать разные никнеймы на разных платформах',
            'Регулярно проверять утечки данных'
        ],
        'sources': [
            'Telegram API',
            'VK API',
            'Публичные базы данных'
        ]
    }
    
    await update.message.reply_text("⏳ Генерирую PDF-отчёт...")
    
    filename = PDFGenerator.generate_osint_report(report_data, 'person')
    
    with open(filename, 'rb') as f:
        await update.message.reply_document(
            document=f,
            filename=filename,
            caption="✅ Ваш OSINT-отчёт готов!",
            reply_markup=main_menu()
        )
    
    os.remove(filename)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена сценария"""
    await update.message.reply_text("❌ Действие отменено.", reply_markup=main_menu())
    return ConversationHandler.END

async def cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена через callback"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("❌ Отменено.", reply_markup=main_menu())
    return ConversationHandler.END
