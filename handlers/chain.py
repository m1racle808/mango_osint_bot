from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from keyboards import chain_action_buttons, main_menu
from states import *
from pdf_generator import PDFGenerator
from subscription import require_subscription
from chain_builder import ChainBuilder
import states

async def chain_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало логической цепочки"""
    if not await require_subscription(update, context):
        return ConversationHandler.END
    
    # Инициализируем построитель цепочки
    context.user_data['chain_builder'] = ChainBuilder()
    
    await update.message.reply_text(
        "🔗 <b>Логическая цепочка OSINT</b>\n\n"
        "Введите первый элемент для поиска:\n"
        "• Email (user@example.com)\n"
        "• Номер телефона (+7 999 123-45-67)\n"
        "• Username (nickname)\n\n"
        "Бот предложит варианты дальнейших действий.",
        parse_mode='HTML'
    )
    return states.CHAIN_START_INPUT

async def chain_process_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ввода первого элемента"""
    user_input = update.message.text
    context.user_data['current_input'] = user_input
    
    builder: ChainBuilder = context.user_data['chain_builder']
    actions = builder.get_available_actions(user_input)
    
    # Добавляем начальный шаг
    builder.add_step(user_input, "Начальный ввод", "start")
    
    await update.message.reply_text(
        f"📥 <b>Получено:</b> {user_input}\n\n"
        f"<b>Что делаем дальше?</b>",
        parse_mode='HTML',
        reply_markup=chain_action_buttons(actions)
    )
    return states.CHAIN_ACTIONS

async def chain_handle_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка выбранного действия в цепочке"""
    query = update.callback_query
    await query.answer()
    
    action = query.data
    
    if action == "finish_chain":
        # Завершаем цепочку и генерируем PDF
        builder: ChainBuilder = context.user_data['chain_builder']
        chain_data = builder.get_chain_data()
        final_findings = builder.get_final_findings()
        
        await query.edit_message_text("⏳ Генерирую PDF со схемой расследования...")
        
        filename = PDFGenerator.generate_chain_report(chain_data, final_findings)
        
        with open(filename, 'rb') as f:
            await query.message.reply_document(
                document=f,
                filename=filename,
                caption="✅ Ваша логическая цепочка готова!",
                reply_markup=main_menu()
            )
        
        os.remove(filename)
        builder.reset()
        return ConversationHandler.END
    
    elif action == "cancel":
        await query.edit_message_text("❌ Отменено.", reply_markup=main_menu())
        return ConversationHandler.END
    
    else:
        # Обрабатываем выбранное действие
        builder: ChainBuilder = context.user_data['chain_builder']
        current_input = context.user_data.get('current_input', '')
        
        result = builder.process_action(action, current_input)
        
        # Обновляем текущий ввод для следующего шага
        context.user_data['current_input'] = result['findings']
        
        await query.edit_message_text(
            f"🔍 <b>Результат:</b>\n{result['findings']}\n\n"
            f"<b>Следующие шаги:</b>",
            parse_mode='HTML',
            reply_markup=chain_action_buttons(result['next_actions'])
        )
        return states.CHAIN_ACTIONS

async def chain_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена цепочки"""
    await update.message.reply_text("❌ Построение цепочки отменено.", reply_markup=main_menu())
    return ConversationHandler.END
