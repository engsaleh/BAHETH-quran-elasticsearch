

# 🚀 دليل البدء السريع — تطبيق البحث في القرآن الكريم



## 🧩 المتطلبات الأساسية

قبل البدء، تأكد من توفر المتطلبات التالية على جهازك:

- Python ≥ 3.8  
- Elasticsearch ≥ 8.x

---

## الخطوة 1: تثبيت وتشغيل Elasticsearch

###  على Ubuntu / Debian

# إضافة مستودع Elasticsearch
```
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
```

# تثبيت وتشغيل الخدمة
sudo apt-get update && sudo apt-get install elasticsearch
sudo systemctl start elasticsearch

# حفظ كلمة المرور التي تظهر في السجلات
```
sudo journalctl -u elasticsearch | grep "password"
```



###  على macOS

````
brew tap elastic/tap
brew install elastic/tap/elasticsearch-full
elasticsearch
```

ستظهر كلمة المرور مباشرة في نافذة Terminal.

### على Windows

1. نزّل Elasticsearch من: [elastic.co/downloads/elasticsearch](https://www.elastic.co/downloads/elasticsearch)
2. فك الضغط عن الملف وشغّل:

   ```
   bin\elasticsearch.bat
   ```
3. احفظ كلمة المرور الظاهرة في نافذة التشغيل.



## الخطوة 2: إعداد المشروع

```
git clone https://github.com/<your-user>/quran-search-app.git
cd quran-search-app

# إنشاء بيئة افتراضية
python -m venv venv

# تفعيل البيئة
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# تثبيت المتطلبات
pip install -r requirements.txt
```



## الخطوة 3: إعداد ملف البيئة

أنشئ ملفًا باسم `.env` في جذر المشروع يحتوي على القيم التالية:

```env
ES_URL=https://localhost:9200
ES_USER=elastic
ES_PASS=كلمة_المرور_التي_حفظتها
ES_INDEX=quran_search_v1
```

## الخطوة 4: تحضير البيانات

إذا كان لديك ملف XML خام:

```bash
python prepare_quran_data.py
```

أو تأكد من وجود ملف `quran_data.csv` بتنسيق صحيح قبل الفهرسة.



## الخطوة 5: إنشاء الفهرس وفهرسة البيانات

```bash
python setup_index.py
```

قد تستغرق العملية من 2 إلى 5 دقائق حسب أداء جهازك.



## الخطوة 6: تشغيل التطبيق

```bash
python app.py
```

ثم افتح المتصفح على العنوان التالي:  **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

## اختبار سريع

### اختبار تلقائي

```bash
python test_search.py
```

### اختبار تفاعلي

```bash
python test_search.py --interactive
```

### تنفيذ بحث مباشر

```bash
python test_search.py --query "الصلاة" --type hybrid --top-k 5
```



## 🛠️ المشاكل الشائعة وحلولها

### ❌ `Connection refused` أو `Connection error`

تحقق من أن Elasticsearch يعمل:

```bash
curl -X GET "localhost:9200"
```

إذا لم يكن يعمل:

```bash
# Linux
sudo systemctl start elasticsearch
# macOS/Windows
elasticsearch
```



### ❌ `Authentication failed`

تأكد من كلمة المرور الصحيحة في ملف `.env`
للحصول على كلمة المرور:

```bash
sudo grep "elastic" /var/log/elasticsearch/elasticsearch.log | grep "password"
```

أو أعد تعيينها:

```bash
sudo /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
```



### ❌ `Index not found`

شغّل سكريبت إعداد الفهرس:

```bash
python setup_index.py
```



### ❌ البحث الدلالي لا يعمل

تأكد من تثبيت المكتبات التالية:

```bash
pip install sentence-transformers torch
```

قد يستغرق أول تحميل للنموذج عدة دقائق.

## 💬 الدعم الفني

إذا واجهت مشكلة:

1. راجع قسم المشاكل الشائعة أعلاه.
2. تحقق من سجلات الـ Terminal.
3. افتح Issue في GitHub مع وصف دقيق للمشكلة.


 استخدم الأمر التالي لتشخيص الأخطاء تلقائيًا:

 ```
python test_search.py
 ```


