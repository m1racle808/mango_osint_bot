import os
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from config import BOT_TOKEN
from handlers import menu, report, chain
from states import *

def main():
    """Запуск бота"""
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрация обработчиков команд
    app.add_handler(CommandHandler("start", menu.start))
    
    # Регистрация обработчика кнопки "Помощь"
    app.add_handler(MessageHandler(filters.Regex("ℹ️ Помощь"), menu.help_command))
    
    # ConversationHandler для OSINT-отчёта
    report_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("📊 OSINT-отчёт"), report.report_start)],
        states={
            REPORT_TYPE: [CallbackQueryHandler(report.report_type_choice)],
            REPORT_PERSON_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, report.get_person_name)],
            REPORT_PERSON_NICK: [MessageHandler(filters.TEXT & ~filters.COMMAND, report.get_person_nick)],
            REPORT_PERSON_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, report.get_person_city)],
            REPORT_COMPANY_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u,c: None)],  # Демо
            REPORT_COMPANY_INN: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u,c: None)],
            REPORT_COMPANY_SITE: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u,c: None)],
            REPORT_PROJECT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u,c: None)],
            REPORT_PROJECT_REPO: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u,c: None)],
            REPORT_PROJECT_DOMAIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u,c: None)],
        },
        fallbacks=[
            CallbackQueryHandler(report.cancel_callback, pattern="cancel"),
            MessageHandler(filters.Regex("❌ Отмена"), report.cancel)
        ],
        allow_reentry=True
    )
    
    # ConversationHandler для логической цепочки
    chain_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("🔗 Логическая цепочка"), chain.chain_start)],
        states={
            CHAIN_START_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, chain.chain_process_input)],
            CHAIN_ACTIONS: [CallbackQueryHandler(chain.chain_handle_action)],
        },
        fallbacks=[
            MessageHandler(filters.Regex("❌ Отмена"), chain.chain_cancel),
            CallbackQueryHandler(report.cancel_callback, pattern="cancel")
        ],
        allow_reentry=True
    )
    
    app.add_handler(report_conv)
    app.add_handler(chain_conv)
    
    # Обработчик кнопки "Вернуться в меню"
    app.add_handler(CallbackQueryHandler(menu.start, pattern="back_to_menu"))
    
    # Обработчик проверки подписки
    from subscription import check_subscription
    from keyboards import main_menu
    
    async def check_sub_callback(update, context):
        query = update.callback_query
        await query.answer()
        from subscription import check_subscription as check_sub
        if await check_sub(update.effective_user.id, context):
            await query.edit_message_text("✅ Спасибо за подписку! Теперь вы можете пользоваться ботом.", reply_markup=main_menu())
        else:
            await query.edit_message_text("❌ Вы всё ещё не подписаны. Пожалуйста, подпишитесь на канал.", 
                                         reply_markup=subscription.check_subscription_button())
    
    app.add_handler(CallbackQueryHandler(check_sub_callback, pattern="check_sub"))
    
    print("🤖 Бот Mango Instruments - OSINT запущен!")
    app.run_polling()

if __name__ == "__main__":
    import os
    # Добавляем импорт os для удаления файлов
    import os as _os
    globals()['os'] = _os
    main()
