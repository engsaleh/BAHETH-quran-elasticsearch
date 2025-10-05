# 🕌 تطبيق البحث في القرآن الكريم

تطبيق ويب متقدم للبحث في القرآن الكريم باستخدام تقنيات البحث اللغوي والدلالي، مبني بـ Flask و Elasticsearch.

## ✨ المميزات

- 🔍 **ثلاثة أنواع من البحث:**

 - **لغوي (Lexical)**: بحث دقيق يطابق الكلمات والنصوص
 - **دلالي (Semantic)**: بحث ذكي يفهم المعاني والسياق
 - **هجين (Hybrid)**: يجمع بين النوعين للحصول على أفضل النتائج

- 🎨 **واجهة مستخدم عصرية وسهلة الاستخدام**
- 🌐 **دعم كامل للغة العربية** مع اتجاه من اليمين لليسار
- ⚡ **أداء عالي** مع Elasticsearch
- 📱 **تصميم متجاوب** يعمل على جميع الأجهزة
- 🔢 **عرض درجة الدقة** لكل نتيجة بحث

## 📋 المتطلبات

### البرمجيات المطلوبة:

1. **Python 3.8+**
2. **Elasticsearch 8.x** (يمكن تشغيله محلياً أو استخدام خدمة سحابية)
3. **pip** لإدارة الحزم

## 🚀 التثبيت والإعداد

### الخطوة 1: تثبيت Elasticsearch

#### على Ubuntu/Debian:

```bash
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
sudo apt-get update && sudo apt-get install elasticsearch
```

#### على macOS:

```bash
brew tap elastic/tap
brew install elastic/tap/elasticsearch-full
```

#### على Windows:

قم بتحميل وتثبيت Elasticsearch من [الموقع الرسمي](https://www.elastic.co/downloads/elasticsearch)

### الخطوة 2: تشغيل Elasticsearch

```bash
# على Linux/macOS
sudo systemctl start elasticsearch

# أو
elasticsearch

# تحقق من التشغيل
curl -X GET "localhost:9200"
```

### الخطوة 3: تحميل المشروع

```bash
# استنسخ المشروع
git clone <repository-url>
cd quran-search-app

# أنشئ بيئة افتراضية
python -m venv venv

# فعّل البيئة الافتراضية
# على Linux/macOS:
source venv/bin/activate

# على Windows:
venv\Scripts\activate
```

### الخطوة 4: تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

### الخطوة 5: إعداد متغيرات البيئة

أنشئ ملف `.env` في المجلد الرئيسي:

```env
ES_URL=https://localhost:9200
ES_USER=elastic
ES_PASS=your_elasticsearch_password
ES_INDEX=quran_search_v1
```

**ملاحظة**: احصل على كلمة المرور من إعدادات Elasticsearch أو من ملف التسجيل عند أول تشغيل.

### الخطوة 6: تحضير البيانات

تأكد من وجود ملف `quran_data.csv` في المجلد الرئيسي بالتنسيق التالي:

```csv
sura,aya,text,sura_name
1,1,بِسْمِ اللَّهِ الرَّحْمَـٰنِ الرَّحِيمِ,الفاتحة
1,2,الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ,الفاتحة
...
```

إذا كان لديك ملف XML، يمكنك استخدام:

```bash
python prepare_quran_data.py
```

### الخطوة 7: إنشاء الفهرس وفهرسة البيانات

```bash
python setup_index.py
```

هذا السكريبت سيقوم بـ:

- إنشاء فهرس Elasticsearch
- فهرسة جميع آيات القرآن
- توليد embeddings للبحث الدلالي
- التحقق من نجاح العملية

### الخطوة 8: تشغيل التطبيق

```bash
python app.py
```

افتح المتصفح على: `http://127.0.0.1:5000`

## 📖 كيفية الاستخدام

### 1. البحث الأساسي

- أدخل النص الذي تريد البحث عنه
- اختر نوع البحث (يُنصح بالبحث الهجين)
- حدد عدد النتائج المطلوبة
- اضغط على "بحث"

### 2. أنواع البحث

#### البحث اللغوي (Lexical)

مناسب للبحث عن:

- كلمات محددة
- عبارات دقيقة
- أسماء السور

مثال: `الصلاة` - سيجد جميع الآيات التي تحتوي على كلمة "الصلاة"

#### البحث الدلالي (Semantic)

مناسب للبحث عن:

- مفاهيم ومعاني
- مواضيع
- أسئلة

مثال: `الصبر على المصائب` - سيجد آيات تتحدث عن الصبر حتى لو لم تحتوِ على هذه الكلمات بالضبط

#### البحث الهجين (Hybrid) - الموصى به

يجمع بين مميزات النوعين السابقين للحصول على أفضل النتائج.

### 3. فهم النتائج

كل نتيجة تعرض:

- **اسم السورة ورقمها**
- **رقم الآية**
- **نص الآية كاملاً**
- **درجة الدقة**: كلما كانت أعلى، كانت النتيجة أكثر صلة

## 🔧 الملفات الرئيسية

```
quran-search-app/
├── app.py                      # تطبيق Flask الرئيسي
├── quran_search_backend.py     # منطق البحث والاتصال بـ ES
├── index_mapping.py            # تعريف بنية الفهرس
├── setup_index.py              # سكريبت الإعداد
├── prepare_quran_data.py       # تحضير البيانات من XML
├── requirements.txt            # المتطلبات البرمجية
├── .env                        # متغيرات البيئة (لا تشاركه!)
├── quran_data.csv             # بيانات القرآن
├── templates/
│   └── index.html             # واجهة المستخدم
└── README.md                  # هذا الملف
```

## 🔌 API Endpoints

### البحث

```
POST /api/search
Content-Type: application/json

{
 "query": "نص البحث",
 "search_type": "hybrid|lexical|semantic",
 "top_k": 10
}
```

**Response:**

```json
{
 "success": true,
 "results": [
 {
 "sura": 1,
 "aya": 1,
 "text": "بِسْمِ اللَّهِ الرَّحْمَـٰنِ الرَّحِيمِ",
 "sura_name": "الفاتحة",
 "score": 15.234
 }
 ],
 "count": 10,
 "query": "نص البحث",
 "search_type": "hybrid"
}
```

### فحص الحالة

```
GET /api/health
```

### الإحصائيات

```
GET /api/stats
```

## 🐛 حل المشاكل الشائعة

### مشكلة: فشل الاتصال بـ Elasticsearch

**الحل:**

1. تأكد من تشغيل Elasticsearch: `curl localhost:9200`
2. تحقق من إعدادات `.env`
3. تأكد من كلمة المرور الصحيحة

### مشكلة: بطء البحث الدلالي

**الحل:**

1. النموذج يُحمّل عند أول استخدام (قد يأخذ وقتاً)
2. تأكد من وجود ذاكرة كافية (4GB+ يُنصح بها)
3. استخدم نموذج أصغر في `quran_search_backend.py`

### مشكلة: لا تظهر النتائج

**الحل:**

1. تأكد من تشغيل `setup_index.py` أولاً
2. تحقق من وجود البيانات: `GET /api/stats`
3. راجع سجلات الأخطاء في terminal

## 🚀 النشر في الإنتاج

### استخدام Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### استخدام Docker (قريباً)

سيتم إضافة Dockerfile قريباً للنشر السهل.

## 🔒 أمان الإنتاج

⚠️ **مهم للإنتاج:**

1. **استخدم HTTPS** لتشفير الاتصال
2. **فعّل المصادقة** على Elasticsearch
3. **استخدم شهادات SSL صالحة**
4. **أزل `verify_certs=False`** من الكود
5. **لا تشارك ملف `.env`**
6. **استخدم كلمات مرور قوية**

## 📈 تحسينات مستقبلية

- [ ] إضافة دعم الترجمة الإنجليزية في البحث
- [ ] إضافة البحث بالجذور اللغوية (lemma)
- [ ] إضافة فلاتر (بالسورة، الجزء، الصفحة)
- [ ] إضافة تصدير النتائج
- [ ] إضافة حفظ عمليات البحث المفضلة
- [ ] دعم تشغيل التلاوة الصوتية
- [ ] إضافة التفسير

## 🤝 المساهمة

المساهمات مرحب بها! يرجى:

1. Fork المشروع
2. إنشاء branch جديد (`git checkout -b feature/amazing-feature`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push للـ branch (`git push origin feature/amazing-feature`)
5. فتح Pull Request

## 📝 الترخيص

هذا المشروع مفتوح المصدر ومتاح للاستخدام التعليمي والشخصي.

## 👥 المطورون

تم تطويره بواسطة فريق التطوير - إذا أعجبك المشروع، لا تنسَ إعطاءه ⭐

## 📞 الدعم

إذا واجهت أي مشاكل:

1. تحقق من قسم حل المشاكل أعلاه
2. ابحث في Issues الموجودة
3. افتح Issue جديد مع تفاصيل المشكلة

---

بالتأكيد، إليك ملف ملاحظة (README/مستند توثيقي) احترافي يوثق مصدر البيانات وطريقة تحويلها.

---

# توثيق مصدر البيانات وتحضيرها

## 📜 نظرة عامة

يوثّق هذا المستند مصدر البيانات القرآنية المستخدمة في هذا المشروع والخطوات المتبعة لتحويلها من صيغة XML إلى صيغة CSV، مما يسهل معالجتها واستخدامها في التطبيقات التحليلية والبرمجية.

---

## 💾 مصدر البيانات القرآنية

تم استخدام ملف البيانات النصية البسيط للقرآن الكريم (بدون تشكيل)، وهو الملف المُسمى **`quran-simple-plain.xml`**.

- **المصدر:** موقع تنزيل (Tanzil.net).
- **رابط التحميل:** [https://tanzil.net/download/](https://tanzil.net/download/)
- **الترخيص:** يُرجى مراجعة شروط استخدام موقع تنزيل للبيانات الخاصة بهم.

---

## 🛠️ عملية تحويل البيانات (XML إلى CSV)

تم تحويل ملف البيانات **`quran-simple-plain.xml`** إلى ملف بصيغة CSV مُنظّمة، وهو الملف المُسمى **`quran_data.csv`**، باستخدام السكربت المخصص **`prepare_quran_data.py`** الموضح أدناه.

### 📝 سكربت التحويل: `prepare_quran_data.py`

يستخدم السكربت مكتبتي `xml.etree.ElementTree` لمعالجة XML و `pandas` لتكوين وإخراج ملف CSV.

```python
import xml.etree.ElementTree as ET
import pandas as pd
import re

def remove_arabic_diacritics(text):
 """إزالة التشكيل من النص العربي"""
 if not text:
  return ""
 # يُستخدم هذا الفانكشن لإزالة علامات التشكيل، ولكنه غير مُفعّل في الإخراج الحالي للـ CSV.
 return re.sub(r'[\u064b-\u0652\u0670]', '', text)

def generate_csv_from_xml(xml_file_path="data/quran-simple-plain.xml", output_csv_path="quran_data.csv"):
 """
 يقوم بتحويل البيانات من ملف XML إلى DataFrame ومن ثم إلى ملف CSV.
 """
 tree = ET.parse(xml_file_path)
 root = tree.getroot()

 records = []
 for sura in root.findall('sura'):
  sura_index = int(sura.get('index'))
  sura_name = sura.get('name')

  for aya in sura.findall('aya'):
   aya_index = int(aya.get('index'))
   text = aya.get('text')
   bismillah = aya.get('bismillah', '') # لالتقاط البسملة إن وجدت كخاصية منفصلة

   record = {
     "sura": sura_index,
     "aya": aya_index,
     "text": text,
     "sura_name": sura_name,
     # يمكن إضافة حقول أخرى هنا في حال إضافة بيانات إضافية (مثل الترجمة، الجزر اللغوية، إلخ.)
   }
   records.append(record)

 df = pd.DataFrame(records)
 # يتم تصدير البيانات إلى ملف CSV باستخدام ترميز 'utf-8-sig' لضمان التعامل السليم مع الحروف العربية.
 df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
 print(f"✅ تم إنشاء ملف CSV بنجاح في: {output_csv_path}")

if __name__ == "__main__":
 # يُفترض أن الملف الأصلي موجود في المسار "data/quran-simple-plain.xml"
 generate_csv_from_xml()
```

### 📋 حقول ملف الـ CSV الناتج

يحتوي ملف **`quran_data.csv`** على الأعمدة التالية:

| العمود          | الوصف                           | نوع البيانات |
| :-------------- | :------------------------------ | :----------- |
| **`sura`**      | رقم السورة (الفهرس)             | عدد صحيح     |
| **`aya`**       | رقم الآية ضمن السورة (الفهرس)   | عدد صحيح     |
| **`text`**      | النص القرآني للآية (بدون تشكيل) | نص (String)  |
| **`sura_name`** | اسم السورة باللغة العربية       | نص (String)  |

هذا التنسيق المُنظَّم يتيح سهولة البحث، الفهرسة، والربط مع أي مصادر بيانات أخرى.

