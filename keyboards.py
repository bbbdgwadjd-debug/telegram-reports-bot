from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def get_main_menu_keyboard():
    """لوحة المفاتيح الرئيسية"""
    keyboard = [
        [InlineKeyboardButton("➕ إضافة حساب", callback_data="add_account")],
        [InlineKeyboardButton("📝 بدء الإبلاغ", callback_data="start_report")],
        [InlineKeyboardButton("👨‍💻 المطور", callback_data="dev_info")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_report_menu_keyboard():
    """لوحة مفاتيح قائمة الإبلاغات"""
    keyboard = [
        [InlineKeyboardButton("🏷️ الكليشه", callback_data="select_category")],
        [InlineKeyboardButton("📌 الموضوع", callback_data="select_topic")],
        [InlineKeyboardButton("🔗 رابط المنشور والقناة", callback_data="select_links")],
        [InlineKeyboardButton("⚠️ المخالفات", callback_data="select_violations")],
        [InlineKeyboardButton("⏱️ عدد التأخيرات", callback_data="select_delay")],
        [InlineKeyboardButton("📊 عدد الإبلاغات", callback_data="select_report_count")],
        [InlineKeyboardButton("✅ إرسال الإبلاغ", callback_data="submit_report")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_category_keyboard():
    """لوحة مفاتيح اختيار الكليشه"""
    keyboard = [
        [InlineKeyboardButton("📰 أخبار", callback_data="cat_news")],
        [InlineKeyboardButton("🎬 محتوى", callback_data="cat_content")],
        [InlineKeyboardButton("💬 تعليقات", callback_data="cat_comments")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_report")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_violations_keyboard():
    """لوحة مفاتيح اختيار المخالفات"""
    keyboard = [
        [InlineKeyboardButton("❌ محتوى مسيء", callback_data="viol_offensive")],
        [InlineKeyboardButton("🚫 محتوى محظور", callback_data="viol_banned")],
        [InlineKeyboardButton("🎭 انتحال", callback_data="viol_impersonation")],
        [InlineKeyboardButton("📢 بريد عشوائي", callback_data="viol_spam")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_report")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard():
    """لوحة مفاتيح الرجوع البسيطة"""
    keyboard = [
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_dev_keyboard():
    """لوحة مفاتيح معلومات المطور"""
    keyboard = [
        [InlineKeyboardButton("👨‍💻 المطور", url="https://t.me/isszo")],
        [InlineKeyboardButton("📢 القناة", url="https://t.me/zzxa100")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_confirm_keyboard():
    """لوحة تأكيد"""
    keyboard = [
        [InlineKeyboardButton("✅ تأكيد", callback_data="confirm")],
        [InlineKeyboardButton("❌ إلغاء", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)
