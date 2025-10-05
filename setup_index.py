#!/usr/bin/env python3
"""
سكريبت لإعداد فهرس Elasticsearch وفهرسة بيانات القرآن الكريم
يجب تشغيل هذا الملف مرة واحدة قبل بدء التطبيق
"""

import sys
import quran_search_backend as quran_es

def main():
    print("\n" + "="*70)
    print(" بدء إعداد فهرس البحث في القرآن الكريم")
    print("="*70 + "\n")

    # التحقق من الاتصال بـ Elasticsearch
    if quran_es.es is None:
        print(" فشل الاتصال بـ Elasticsearch")
        print(" تأكد من:")
        print("   1. تشغيل خادم Elasticsearch")
        print("   2. صحة الإعدادات في ملف .env")
        print("   3. اتصالك بالشبكة إذا كان Elasticsearch على خادم بعيد")
        sys.exit(1)

    try:
        if not quran_es.es.ping():
            print(" لا يمكن الاتصال بـ Elasticsearch")
            sys.exit(1)
    except Exception as e:
        print(f" خطأ في الاتصال: {str(e)}")
        sys.exit(1)

    print(" الاتصال بـ Elasticsearch ناجح\n")

    # الخطوة 1: إنشاء الفهرس
    print(" الخطوة 1: إنشاء الفهرس")
    print("-" * 70)

    try:
        # التحقق من وجود فهرس قديم
        if quran_es.es.indices.exists(index=quran_es.INDEX_NAME):
            print(f"  الفهرس '{quran_es.INDEX_NAME}' موجود مسبقاً")
            response = input("هل تريد حذفه وإنشاءه من جديد؟ (y/n): ")

            if response.lower() != 'y':
                print(" تم إلغاء العملية")
                sys.exit(0)

        quran_es.create_quran_index()
        print(" تم إنشاء الفهرس بنجاح\n")

    except Exception as e:
        print(f" فشل إنشاء الفهرس: {str(e)}")
        sys.exit(1)

    # الخطوة 2: فهرسة البيانات
    print(" الخطوة 2: فهرسة بيانات القرآن الكريم")
    print("-" * 70)

    # التحقق من وجود ملف البيانات
    import os
    csv_file = "quran_data.csv"

    if not os.path.exists(csv_file):
        print(f" ملف البيانات '{csv_file}' غير موجود")
        print(" تأكد من وجود الملف في نفس المجلد أو قم بتوليده أولاً")
        sys.exit(1)

    try:
        quran_es.index_quran_data(csv_file)
        print("\n تم فهرسة البيانات بنجاح")

    except Exception as e:
        print(f"\n فشلت عملية الفهرسة: {str(e)}")
        sys.exit(1)

    # الخطوة 3: التحقق من الفهرسة
    print("\n الخطوة 3: التحقق من الفهرسة")
    print("-" * 70)

    try:
        count = quran_es.es.count(index=quran_es.INDEX_NAME)
        total_verses = count['count']

        print(f" عدد الآيات المفهرسة: {total_verses}")

        if total_verses > 0:
            print("\n تم إعداد الفهرس بنجاح!")
            print("يمكنك الآن تشغيل التطبيق باستخدام: python app.py")
        else:
            print("\n  الفهرس فارغ. يرجى التحقق من ملف البيانات")

    except Exception as e:
        print(f"  خطأ في التحقق: {str(e)}")

    print("\n" + "="*70)
    print("انتهى الإعداد")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
