#!/bin/bash

echo "🔧 شروع نصب پیش‌نیازهای پروژه monitorlv ..."

# به‌روزرسانی لیست پکیج‌ها
sudo apt update

# نصب پایتون، pip و ابزارهای شبکه
sudo apt install -y python3 python3-pip iputils-ping snmp snmp-mibs-downloader

# فعال‌سازی MIB برای خوانایی بهتر (اختیاری)
sudo download-mibs

# نصب کتابخانه‌های پایتونی
pip3 install -r requirements.txt

echo "✅ نصب کامل شد. برای اجرا دستور زیر را وارد کنید:"
echo "python3 run_all.py"
