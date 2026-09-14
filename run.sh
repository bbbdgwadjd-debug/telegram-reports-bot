#!/bin/bash

# تثبيت المتطلبات
echo "📦 تثبيت المتطلبات..."
pip install -r requirements.txt

# إنشاء ملف .env من المثال
if [ ! -f .env ]; then
    echo "📝 إنشاء ملف .env..."
    cp .env.example .env
    echo "⚠️  قم بتعديل ملف .env وأضف البيانات المطلوبة"
fi

# بدء البوت
echo "🚀 بدء البوت..."
python main.py