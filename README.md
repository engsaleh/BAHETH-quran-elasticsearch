# باحث BAHETH محرك بحث قرآني متقدم باستخدام Elasticsearch  

تطبيق ويب احترافي للبحث الذكي في القرآن الكريم يجمع بين قوة Elasticsearch وتقنيات الذكاء الاصطناعي لتوفير تجربة بحث متقدمة بثلاثة أنماط: اللغوي 
والدلالي والهجين.)
## 📑 المحتويات

- [نظرة عامة](https://claude.ai/chat/4c9cddcc-01e4-4331-900e-8666151444c8#-نظرة-عامة)
- [المميزات الرئيسية](https://claude.ai/chat/4c9cddcc-01e4-4331-900e-8666151444c8#-المميزات-الرئيسية)
- [البنية التقنية](https://claude.ai/chat/4c9cddcc-01e4-4331-900e-8666151444c8#-البنية-التقنية)
- [المتطلبات](https://claude.ai/chat/4c9cddcc-01e4-4331-900e-8666151444c8#-المتطلبات)
- [التثبيت والإعداد](https://claude.ai/chat/4c9cddcc-01e4-4331-900e-8666151444c8#-التثبيت-والإعداد)
- [دليل الاستخدام](https://claude.ai/chat/4c9cddcc-01e4-4331-900e-8666151444c8#-دليل-الاستخدام)
- [API Documentation](https://claude.ai/chat/4c9cddcc-01e4-4331-900e-8666151444c8#-api-documentation)
- [مصدر البيانات](https://claude.ai/chat/4c9cddcc-01e4-4331-900e-8666151444c8#-مصدر-البيانات)
- [حل المشاكل](https://claude.ai/chat/4c9cddcc-01e4-4331-900e-8666151444c8#-حل-المشاكل)
- [المساهمة](https://claude.ai/chat/4c9cddcc-01e4-4331-900e-8666151444c8#-المساهمة)

------

## 🎯 نظرة عامة

يوفر هذا المشروع محرك بحث متطور للقرآن الكريم (6,236 آية) باستخدام تقنيات حديثة تجمع بين:

- **البحث اللغوي (Lexical)**: مطابقة دقيقة للكلمات باستخدام خوارزمية BM25
- **البحث الدلالي (Semantic)**: فهم المعاني والسياق باستخدام Sentence Transformers
- **البحث الهجين (Hybrid)**: دمج ذكي بين النوعين السابقين

### الهدف من المشروع

بناء نظام بحث ذكي يتجاوز المطابقة النصية التقليدية ليفهم المعاني والسياق، مع دعم:

- المترادفات والمشتقات اللغوية
- الأخطاء الإملائية
- البحث المفاهيمي والموضوعي

------

## ✨ المميزات الرئيسية

### البحث المتقدم

-  ثلاثة أنماط بحث قابلة للتبديل الفوري
-  ذكاء اصطناعي لفهم المعاني (384-dimensional embeddings)
-  درجات ملاءمة دقيقة لكل نتيجة
-  أداء عالي (استجابة أقل من 200ms للبحث الهجين)

### الواجهة والتجربة

-  تصميم إسلامي عصري بألوان خضراء وذهبية
-  دعم كامل للعربية RTL مع خط Amiri لعرض الآيات
-  متجاوب تماماً على جميع الأجهزة
-  UX محسّن مع animations سلسة

### التقنيات

-  محلل عربي متقدم مع stemming وتقييس normalization
-  اتصال آمن مع Elasticsearch
-  API RESTful موثقة 
-  قابل للاختبار مع test suite متكامل

------

## 🏗️ البنية التقنية

### Stack التقني

| المكون                | التقنية               | الإصدار |
| --------------------- | --------------------- | ------- |
| **Backend Framework** | Flask                 | 3.0.0   |
| **محرك البحث**        | Elasticsearch         | 9.1.4   |
| **نماذج AI**          | Sentence Transformers | 2.2.2   |
| **معالجة البيانات**   | Pandas                | 2.1.4+  |
| **Frontend**          | HTML5/CSS3/Vanilla JS | -       |

### المعمارية

```
┌─────────────────┐
│   المستخدم      │
└────────┬────────┘
         │
    ┌────▼─────┐
    │  Flask   │
    │  Server  │
    └────┬─────┘
         │
    ┌────▼──────────────────┐
    │  quran_search_backend │
    └────┬──────────────────┘
         │
    ┌────▼────────┬──────────────┐
    │             │              │
┌───▼───┐    ┌───▼───┐    ┌────▼────┐
│BM25   │    │ kNN   │    │ Hybrid  │
│Search │    │Search │    │ Fusion  │
└───┬───┘    └───┬───┘    └────┬────┘
    │            │             │
    └────────────▼─────────────┘
                 │
         ┌───────▼────────┐
         │ Elasticsearch  │
         │  Index (25MB)  │
         └────────────────┘
```

------

## 📋 المتطلبات

### المتطلبات الأساسية

- Python: 3.8 أو أحدث
- Elasticsearch: 9.1.4 (موصى به) أو 8.x
- الذاكرة: 4GB RAM كحد أدنى (8GB موصى به)
- المساحة: 2GB مساحة فارغة

### المكتبات المطلوبة

```txt
flask==3.0.0
flask-cors==4.0.0
elasticsearch==8.11.0
sentence-transformers==2.2.2
pandas==2.1.4
python-dotenv==1.0.0
urllib3==2.1.0
```

------

## 🚀 التثبيت والإعداد

### 1. تثبيت Elasticsearch

#### Ubuntu/Debian

```bash
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | \
  sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] \
  https://artifacts.elastic.co/packages/9.x/apt stable main" | \
  sudo tee /etc/apt/sources.list.d/elastic-9.x.list

sudo apt-get update && sudo apt-get install elasticsearch
sudo systemctl start elasticsearch
```

#### macOS

```bash
brew tap elastic/tap
brew install elastic/tap/elasticsearch-full
brew services start elasticsearch
```

#### Windows

قم بتحميل وتثبيت من [الموقع الرسمي](https://www.elastic.co/downloads/elasticsearch)

#### التحقق من التشغيل

```bash
curl -X GET "localhost:9200"
```

### 2. إعداد المشروع

```bash
# استنساخ المشروع
git clone https://github.com/username/quran-search-elasticsearch.git
cd quran-search-elasticsearch

# إنشاء بيئة افتراضية
python -m venv venv

# تفعيل البيئة
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate     # Windows

# تثبيت المكتبات
pip install -r requirements.txt
```

### 3. إعداد المتغيرات البيئية

أنشئ ملف `.env`:

```env
# Elasticsearch Configuration
ES_URL=https://localhost:9200
ES_USER=elastic
ES_PASS=your_elasticsearch_password
ES_INDEX=quran_search_v1
ES_TIMEOUT=30

# Flask Configuration
FLASK_DEBUG=False
SECRET_KEY=generate-a-secure-random-key

# Model Configuration
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
EMBEDDING_DIM=384

# Search Weights
HYBRID_LEX_WEIGHT=0.5
HYBRID_SEM_WEIGHT=0.5
```

**⚠️ مهم**: احصل على كلمة مرور Elasticsearch من:

```bash
# إذا كان جديداً
sudo /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic

# من logs عند أول تشغيل
sudo journalctl -u elasticsearch | grep "password"
```

### 4. تحضير البيانات القرآنية

#### تحميل البيانات

```bash
# قم بتحميل quran-simple-plain.xml من:
wget https://tanzil.net/res/text/quran-simple-plain.xml
mkdir -p data
mv quran-simple-plain.xml data/
```

#### تحويل XML إلى CSV

```bash
python prepare_quran_data.py
```

**الإخراج المتوقع:**

```
✅ تم إنشاء ملف CSV بنجاح في: quran_data.csv
📊 الإحصائيات:
   - عدد السور: 114
   - عدد الآيات: 6236
   - حجم الملف: 1.2 MB
```

### 5. إنشاء الفهرس وفهرسة البيانات

```bash
python setup_index.py
```

**العملية تستغرق 5-10 دقائق** وتتضمن:

- إنشاء فهرس بإعدادات عربية محسّنة
- توليد embeddings لـ 6,236 آية
- فهرسة البيانات في Elasticsearch
- التحقق من النجاح

**الإخراج المتوقع:**

```
==================================================
 بدء إعداد فهرس البحث في القرآن الكريم
==================================================

✅ الاتصال بـ Elasticsearch ناجح

 الخطوة 1: إنشاء الفهرس
--------------------------------------------------
✅ تم إنشاء الفهرس 'quran_search_v1' بنجاح.

 الخطوة 2: فهرسة بيانات القرآن الكريم
--------------------------------------------------
📚 جاري فهرسة 6236 آية...
⏳ التقدم: 1000/6236 (16.0%)
⏳ التقدم: 2000/6236 (32.1%)
...
✅ تم فهرسة 6236 آية بنجاح!

 الخطوة 3: التحقق من الفهرسة
--------------------------------------------------
✅ عدد الآيات المفهرسة: 6236

✅ تم إعداد الفهرس بنجاح!
```

### 6. تشغيل التطبيق

```bash
python app.py
```

**افتح المتصفح على**: `http://127.0.0.1:5000`

------

## 📖 دليل الاستخدام

### أنواع البحث الثلاثة

#### 1️⃣ البحث اللغوي Lexical

**الاستخدام الأمثل**: البحث عن كلمات أو عبارات محددة

**أمثلة:**

```
"الصلاة"         → آيات تحتوي: الصلاة، صلاتهم، يصلون
"الرحمن الرحيم"  → مطابقة دقيقة للعبارة
"موسى"          → جميع الآيات عن النبي موسى
```

**المميزات:**

- سريع جداً (20-50ms)
- دقة عالية للمطابقة النصية
- يدعم الأخطاء الإملائية (fuzziness)

#### 2️⃣ البحث الدلالي Semantic

**الاستخدام الأمثل**: البحث عن مواضيع ومفاهيم

**أمثلة:**

```
"الصبر على المحن"      → آيات عن الابتلاء والثبات
"عاقبة الظالمين"       → آيات عن العقوبة والعذاب
"التوكل على الله"     → آيات عن الثقة بالله
```

**المميزات:**

- يفهم المعاني والسياق
- يجد آيات متشابهة في المعنى
- لا يشترط وجود الكلمات نفسها

#### 3️⃣ البحث الهجين Hybrid

**الاستخدام الأمثل**: الاستخدام العام

**كيف يعمل:**

```
الدقة النهائية = (دقة لغوية × 50%) + (دقة دلالية × 50%)
```

**الميزة:**

- يجمع دقة البحث اللغوي وذكاء البحث الدلالي
- أفضل توازن للحالات العامة

### فهم درجة الدقة (Score)

| النطاق        | المعنى  | التفسير                     |
| ------------- | ------- | --------------------------- |
| **15-20+**    | ممتاز   | مطابقة دقيقة جداً (لغوي)     |
| **10-15**     | جيد جداً | مطابقة قوية                 |
| **5-10**      | جيد     | مطابقة مقبولة               |
| **0.85-1.0**  | ممتاز   | تشابه معنوي قوي جداً (دلالي) |
| **0.70-0.85** | جيد     | تشابه معنوي جيد             |

------

## API Documentation

### POST `/api/search`

البحث في القرآن الكريم

**Request:**

```json
{
  "query": "الصبر",
  "search_type": "hybrid",
  "top_k": 10
}
```

**Parameters:**

- `query` (string, required): نص البحث
- `search_type` (string, optional): نوع البحث [`lexical`, `semantic`, `hybrid`]. افتراضي: `hybrid`
- `top_k` (integer, optional): عدد النتائج. افتراضي: `10`, نطاق: `1-100`

**Response:**

```json
{
  "success": true,
  "results": [
    {
      "sura": 2,
      "aya": 153,
      "text": "يا أيها الذين آمنوا استعينوا بالصبر والصلاة",
      "sura_name": "البقرة",
      "score": 12.456
    }
  ],
  "count": 10,
  "query": "الصبر",
  "search_type": "hybrid"
}
```

### GET `/api/health`

فحص حالة الخدمة

**Response:**

```json
{
  "status": "healthy",
  "elasticsearch": true,
  "embedding_model": true,
  "index_name": "quran_search_v1"
}
```

### GET `/api/stats`

إحصائيات الفهرس

**Response:**

```json
{
  "success": true,
  "total_verses": 6236,
  "index_name": "quran_search_v1"
}
```

------

## 💾 مصدر البيانات

### البيانات القرآنية

**المصدر**: [Tanzil.net](https://tanzil.net/download/)
 **الملف**: `quran-simple-plain.xml`
 **النسخة**: Simple مع التشكيل وعلامات التطويل 
 **الترخيص**:  ترخيص مفتوح جزئيًا (Free for use with attribution & no modification).

### بنية البيانات

| الحقل       | النوع   | الوصف                 |
| ----------- | ------- | --------------------- |
| `sura`      | Integer | رقم السورة (1-114)    |
| `aya`       | Integer | رقم الآية             |
| `text`      | String  | نص الآية (بدون تشكيل) |
| `sura_name` | String  | اسم السورة            |

**الإحصائيات:**

- عدد السور: 114
- عدد الآيات: 6,236
- حجم CSV: ~1.2 MB
- حجم الفهرس: ~25-30 MB

## حل المشاكل

### مشكلة: `ConnectionError: Connection refused`

**السبب**: Elasticsearch غير مشتغل

**الحل:**

```bash
# التحقق من الحالة
curl localhost:9200

# تشغيل Elasticsearch
sudo systemctl start elasticsearch  # Linux
brew services start elasticsearch   # macOS
```

### مشكلة: `AuthenticationException`

**السبب**: كلمة مرور خاطئة

**الحل:**

```bash
# إعادة تعيين كلمة المرور
sudo /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic

# تحديث .env بكلمة المرور الجديدة
```

### مشكلة: البحث الدلالي بطيء

**السبب**: تحميل النموذج لأول مرة

**الحل:**

- انتظر 30-60 ثانية عند أول استخدام
- النموذج يُحفظ في الذاكرة بعد ذلك
- للتسريع: استخدم نموذج أصغر في `quran_search_backend.py`

### مشكلة: `IndexNotFoundException`

**السبب**: الفهرس غير موجود

**الحل:**

```bash
python setup_index.py
```

### مشكلة: نتائج غير متوقعة

**تحقق من:**

1. نوع البحث المناسب لاستعلامك
2. صحة البيانات: `GET /api/stats`
3. logs في terminal

## 🤝 المساهمة

المساهمات مرحب بها يرجى اتباع الخطوات:

1. **Fork** المشروع
2. أنشئ **feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit** تغييراتك (`git commit -m 'إضافة ميزة رائعة'`)
4. **Push** للـ branch (`git push origin feature/AmazingFeature`)
5. افتح **Pull Request**

------

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة **MIT License** 

------

## 🙏 شكر وتقدير

- **[Tanzil.net](https://tanzil.net/)** - مصدر البيانات القرآنية
- **[Elasticsearch](https://www.elastic.co/)** - محرك البحث القوي
- **[Sentence Transformers](https://www.sbert.net/)** - نماذج Embeddings
- [مجتمع إتقان](https://community.itqan.dev/) للإلهام وتوفير المعلومات المفيدة



⭐ إذا أعجبك المشروع، لا تنسَ إعطائه نجمة

