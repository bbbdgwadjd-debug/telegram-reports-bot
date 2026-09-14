import logging
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes
)
from telegram import Update
from config import BOT_TOKEN, STAGES
from handlers import (
    start,
    main_menu,
    add_account_start,
    add_account_phone,
    add_account_code,
    add_account_2fa,
    start_report,
    select_report_field,
    submit_report,
    dev_info,
    cancel
)
from input_handlers import (
    handle_phone_input,
    handle_code_input,
    handle_topic_input,
    handle_links_input,
    handle_delay_input,
    handle_report_count_input
)

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# تعريف حالات المحادثة
PHONE, CODE, TWO_FA = range(3)
TOPIC, LINKS, DELAY, REPORT_COUNT = range(4, 8)

def main():
    """بدء البوت"""
    # إنشاء التطبيق
    app = Application.builder().token(BOT_TOKEN).build()
    
    # معالج المحادثة لإضافة الحساب
    add_account_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_account_start, pattern="^add_account$")],
        states={
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_account_phone)],
            CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_account_code)],
            TWO_FA: [CallbackQueryHandler(add_account_2fa, pattern="^2fa_")]
        },
        fallbacks=[CallbackQueryHandler(cancel, pattern="^cancel$")]
    )
    
    # معالج المحادثة للإبلاغات
    report_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_report, pattern="^start_report$")],
        states={
            TOPIC: [
                CallbackQueryHandler(select_report_field, pattern="^select_"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_topic_input)
            ],
            LINKS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_links_input)
            ],
            DELAY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_delay_input)
            ],
            REPORT_COUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_report_count_input)
            ]
        },
        fallbacks=[
            CallbackQueryHandler(cancel, pattern="^cancel$"),
            CallbackQueryHandler(main_menu, pattern="^back_to_main$")
        ]
    )
    
    # إضافة المعالجات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(add_account_handler)
    app.add_handler(report_handler)
    app.add_handler(CallbackQueryHandler(main_menu, pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(select_report_field, pattern="^select_"))
    app.add_handler(CallbackQueryHandler(submit_report, pattern="^submit_report$"))
    app.add_handler(CallbackQueryHandler(dev_info, pattern="^dev_info$"))
    app.add_handler(CallbackQueryHandler(main_menu, pattern="^back_to_main$"))
    
    # بدء البوت
    app.run_polling()

if __name__ == "__main__":
    logger.info("🚀 بدء البوت...")
    main()