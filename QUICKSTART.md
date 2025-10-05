# 🚀 دليل البدء السريع

هذا دليل مختصر لتشغيل تطبيق البحث في القرآن الكريم في أقل من 10 دقائق!

## المتطلبات الأساسية

قبل البدء، تأكد من تثبيت:
- Python 3.8 أو أحدث
- Elasticsearch 8.x

## خطوات التشغيل السريع

### 1. تثبيت وتشغيل Elasticsearch

**على Ubuntu/Debian:**
```bash
# تثبيت Elasticsearch
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
sudo apt-get update && sudo apt-get install elasticsearch

# تشغيل Elasticsearch
sudo systemctl start elasticsearch

# احفظ كلمة المرور التي تظهر في السجلات
sudo journalctl -u elasticsearch | grep "password"
```

**على macOS:**
```bash
# تثبيت باستخدام Homebrew
brew tap elastic/tap
brew install elastic/tap/elasticsearch-full

# تشغيل
elasticsearch

# كلمة المرور ستظهر في Terminal
```

**على Windows:**
1. قم بتحميل Elasticsearch من https://www.elastic.co/downloads/elasticsearch
2. فك الضغط وشغّل `bin\elasticsearch.bat`
3. احفظ كلمة المرور من نافذة Terminal

### 2. إعداد المشروع

```bash
# استنسخ أو قم بتحميل المشروع
cd quran-search-app

# أنشئ بيئة افتراضية
python -m venv venv

# فعّل البيئة
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# ثبّت المتطلبات
pip install -r requirements.txt
```

### 3. إعداد ملف البيئة

أنشئ ملف `.env` مع المحتوى التالي:

```env
ES_URL=https://localhost:9200
ES_USER=elastic
ES_PASS=كلمة_المرور_التي_حفظتها
ES_INDEX=quran_search_v1
```

### 4. تحضير البيانات (إذا لزم الأمر)

إذا كان لديك ملف XML:
```bash
python prepare_quran_data.py
```

أو تأكد من وجود `quran_data.csv` بالتنسيق الصحيح.

### 5. إنشاء الفهرس وفهرسة البيانات

```bash
python setup_index.py
```

انتظر حتى تكتمل العملية (قد تستغرق 2-5 دقائق).

### 6. تشغيل التطبيق

```bash
python app.py
```

### 7. افتح المتصفح

انتقل إلى: **http://127.0.0.1:5000**

🎉 **مبروك! التطبيق يعمل الآن!**

---

## اختبار سريع

لاختبار أن كل شيء يعمل:

```bash
# اختبار تلقائي
python test_search.py

# اختبار تفاعلي
python test_search.py --interactive

# بحث مباشر
python test_search.py --query "الصلاة" --type hybrid --top-k 5
```

---

## المشاكل الشائعة وحلولها السريعة

### ❌ خطأ: `Connection refused` أو `Connection error`

**الحل:**
```bash
# تحقق من تشغيل Elasticsearch
curl -X GET "localhost:9200"

# إذا لم يكن يعمل، شغّله:
# Linux:
sudo systemctl start elasticsearch
# macOS/Windows:
elasticsearch
```

### ❌ خطأ: `Authentication failed`

**الحل:** تأكد من كلمة المرور الصحيحة في `.env`

```bash
# للحصول على كلمة المرور على Linux:
sudo grep "elastic" /var/log/elasticsearch/elasticsearch.log | grep "password"

# أو أعد تعيين كلمة المرور:
sudo /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
```

### ❌ خطأ: `Index not found`

**الحل:** شغّل سكريبت الإعداد:
```bash
python setup_index.py
```

### ❌ البحث الدلالي لا يعمل

**الحل:** تأكد من تثبيت `sentence-transformers`:
```bash
pip install sentence-transformers torch
```

أول مرة قد يستغرق تحميل النموذج بضع دقائق.

---

## أوامر مفيدة

```bash
# فحص حالة Elasticsearch
curl -X GET "localhost:9200/_cluster/health?pretty"

# عرض جميع الفهارس
curl -X GET "localhost:9200/_cat/indices?v"

# حذف فهرس معين
curl -X DELETE "localhost:9200/quran_search_v1"

# عد الوثائق في الفهرس
curl -X GET "localhost:9200/quran_search_v1/_count?pretty"
```

---

## التالي؟

- اقرأ [README.md](README.md) للتفاصيل الكاملة
- جرب أنواع البحث المختلفة
- استكشف API endpoints في `/api/search`

---

## الدعم

إذا واجهت مشكلة:
1. راجع قسم المشاكل الشائعة أعلاه
2. تحقق من سجلات Terminal
3. افتح Issue على GitHub مع تفاصيل المشكلة

**نصيحة:** شغّل `python test_search.py` لتشخيص المشاكل تلقائياً.
