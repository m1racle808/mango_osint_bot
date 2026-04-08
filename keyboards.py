from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню (Reply-кнопки)
def main_menu():
    keyboard = [
        ["📊 OSINT-отчёт", "🔗 Логическая цепочка"],
        ["ℹ️ Помощь"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Инлайн-кнопки выбора типа отчёта
def report_type_buttons():
    keyboard = [
        [InlineKeyboardButton("👤 По личности", callback_data="report_person")],
        [InlineKeyboardButton("🏢 По компании", callback_data="report_company")],
        [InlineKeyboardButton("📁 По проекту", callback_data="report_project")],
        [InlineKeyboardButton("❌ Отмена", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Инлайн-кнопки для логической цепочки (динамические)
def chain_action_buttons(actions):
    keyboard = []
    for action in actions:
        keyboard.append([InlineKeyboardButton(action["name"], callback_data=action["callback"])])
    keyboard.append([InlineKeyboardButton("✅ Завершить цепочку", callback_data="finish_chain")])
    keyboard.append([InlineKeyboardButton("❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(keyboard)

# Кнопка проверки подписки
def check_subscription_button():
    keyboard = [[InlineKeyboardButton("🔐 Проверить подписку", callback_data="check_sub")]]
    return InlineKeyboardMarkup(keyboard)

# Кнопка возврата в меню
def back_to_menu_button():
    keyboard = [[InlineKeyboardButton("🏠 Вернуться в меню", callback_data="back_to_menu")]]
    return InlineKeyboardMarkup(keyboard)
