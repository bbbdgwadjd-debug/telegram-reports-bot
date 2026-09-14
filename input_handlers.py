from telegram import Update, ChatAction
from telegram.ext import ContextTypes
from database import SessionLocal, UserSession
import json

async def handle_phone_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج إدخال رقم الهاتف"""
    user_id = update.effective_user.id
    phone = update.message.text
    db = SessionLocal()
    
    try:
        if not phone.startswith('+'):
            await update.message.reply_text(
                "❌ يجب أن يبدأ رقم الهاتف برمز الدولة (+)\nمثال: +966501234567"
            )
            return "PHONE"
        
        # حفظ رقم الهاتف في الجلسة
        session = db.query(UserSession).filter(
            UserSession.telegram_id == user_id
        ).first()
        
        if not session:
            session = UserSession(
                telegram_id=user_id,
                user_id=user_id,
                stage="phone_entered"
            )
            db.add(session)
        
        data = json.loads(session.data or "{}")
        data["phone"] = phone
        session.data = json.dumps(data)
        db.commit()
        
        await update.message.reply_text(
            f"✅ تم حفظ رقم الهاتف: {phone}\n\n"
            f"🔔 سيتم إرسال كود التحقق إلى هاتفك في اللحظات القادمة.\n"
            f"أرسل الكود الذي ستتلقاه:"
        )
        return "CODE"
    finally:
        db.close()

async def handle_code_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج إدخال الكود"""
    user_id = update.effective_user.id
    code = update.message.text
    db = SessionLocal()
    
    try:
        session = db.query(UserSession).filter(
            UserSession.telegram_id == user_id
        ).first()
        
        if session:
            data = json.loads(session.data or "{}")
            data["code"] = code
            session.data = json.dumps(data)
            db.commit()
        
        await update.message.reply_text(
            f"✅ تم التحقق من الكود بنجاح!\n\n"
            f"هل حسابك عليه تحقق بخطوتين (2FA)؟"
        )
        return "2FA"
    finally:
        db.close()

async def handle_topic_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج إدخال الموضوع"""
    user_id = update.effective_user.id
    topic = update.message.text
    db = SessionLocal()
    
    try:
        session = db.query(UserSession).filter(
            UserSession.telegram_id == user_id
        ).first()
        
        if session:
            data = json.loads(session.data or "{}")
            data["topic"] = topic
            session.data = json.dumps(data)
            db.commit()
        
        await update.message.reply_text(
            f"✅ تم حفظ الموضوع: {topic}\n\n"
            f"🔗 الآن أرسل رابط المنشور ورابط القناة (كل رابط في سطر)"
        )
        return "LINKS"
    finally:
        db.close()

async def handle_links_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج إدخال الروابط"""
    user_id = update.effective_user.id
    text = update.message.text
    links = text.split('\n')
    db = SessionLocal()
    
    try:
        session = db.query(UserSession).filter(
            UserSession.telegram_id == user_id
        ).first()
        
        if session:
            data = json.loads(session.data or "{}")
            if len(links) >= 2:
                data["post_link"] = links[0].strip()
                data["channel_link"] = links[1].strip()
            session.data = json.dumps(data)
            db.commit()
        
        await update.message.reply_text(
            f"✅ تم حفظ الروابط\n\n"
            f"⏱️ الآن أرسل عدد التأخيرات بين كل إبلاغ والآخر (رقم فقط)"
        )
        return "DELAY"
    finally:
        db.close()

async def handle_delay_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج إدخال عدد التأخيرات"""
    user_id = update.effective_user.id
    delay = update.message.text
    db = SessionLocal()
    
    try:
        if not delay.isdigit():
            await update.message.reply_text(
                "❌ الرجاء إدخال رقم صحيح فقط"
            )
            return "DELAY"
        
        session = db.query(UserSession).filter(
            UserSession.telegram_id == user_id
        ).first()
        
        if session:
            data = json.loads(session.data or "{}")
            data["delay_count"] = int(delay)
            session.data = json.dumps(data)
            db.commit()
        
        await update.message.reply_text(
            f"✅ تم حفظ عدد التأخيرات: {delay} ثانية\n\n"
            f"📊 الآن أرسل عدد الإبلاغات الإجمالي"
        )
        return "REPORT_COUNT"
    finally:
        db.close()

async def handle_report_count_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج إدخال عدد الإبلاغات"""
    user_id = update.effective_user.id
    count = update.message.text
    db = SessionLocal()
    
    try:
        if not count.isdigit():
            await update.message.reply_text(
                "❌ الرجاء إدخال رقم صحيح فقط"
            )
            return "REPORT_COUNT"
        
        session = db.query(UserSession).filter(
            UserSession.telegram_id == user_id
        ).first()
        
        if session:
            data = json.loads(session.data or "{}")
            data["total_reports"] = int(count)
            session.data = json.dumps(data)
            db.commit()
        
        await update.message.reply_text(
            f"✅ تم حفظ عدد الإبلاغات: {count}\n\n"
            f"📋 ملخص الإبلاغ:\n"
            f"• الموضوع: {data.get('topic', '---')}\n"
            f"• رابط المنشور: {data.get('post_link', '---')}\n"
            f"• رابط القناة: {data.get('channel_link', '---')}\n"
            f"• عدد التأخيرات: {data.get('delay_count', 0)}\n"
            f"• عدد الإبلاغات: {count}\n\n"
            f"✅ اضغط 'إرسال الإبلاغ' لتأكيد"
        )
        return "READY"
    finally:
        db.close()