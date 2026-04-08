from telegram.ext import ConversationHandler

# Состояния для OSINT-отчёта
(
    REPORT_TYPE,
    REPORT_PERSON_NAME,
    REPORT_PERSON_NICK,
    REPORT_PERSON_CITY,
    REPORT_COMPANY_NAME,
    REPORT_COMPANY_INN,
    REPORT_COMPANY_SITE,
    REPORT_PROJECT_NAME,
    REPORT_PROJECT_REPO,
    REPORT_PROJECT_DOMAIN
) = range(10)

# Состояния для логической цепочки
(
    CHAIN_START_INPUT,
    CHAIN_ACTIONS
) = range(2)
