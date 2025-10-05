# quran_search_backend.py (نسخة محسنة)
# يوفر وظائف الاتصال بـ Elasticsearch والفهرسة والبحث مع تحسينات

import os
import re
import pandas as pd
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers
from sentence_transformers import SentenceTransformer
from index_mapping import mappings
import warnings
import urllib3

# تجاهل تحذيرات SSL للتطوير
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore')

# ========================= تحميل الإعدادات =========================
load_dotenv()

ES_URL = os.getenv("ES_URL", "https://localhost:9200")
ES_USER = os.getenv("ES_USER", "elastic")
ES_PASS = os.getenv("ES_PASS", "")
INDEX_NAME = os.getenv("ES_INDEX", "quran_search_v1")

# ========================= الاتصال بـ Elasticsearch =========================
es = None
try:
    es = Elasticsearch(
        ES_URL,
        basic_auth=(ES_USER, ES_PASS),
        verify_certs=False,  # ⚠️ للتطوير فقط
        request_timeout=30,
        max_retries=3,
        retry_on_timeout=True
    )
    if not es.ping():
        raise ValueError("❌ الاتصال بـ Elasticsearch فشل.")
    print("✅ تم الاتصال بـ Elasticsearch بنجاح.")
except Exception as e:
    print(f"⚠️ فشل الاتصال بـ Elasticsearch: {str(e)}")
    es = None

# ========================= نموذج Embeddings =========================
model = None
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

try:
    # نموذج متعدد اللغات يدعم العربية بشكل أفضل
    model = SentenceTransformer(MODEL_NAME)
    print(f"✅ تم تحميل نموذج Embeddings: {MODEL_NAME}")
except Exception as e:
    print(f"⚠️ خطأ أثناء تحميل نموذج Embeddings: {str(e)}")
    print("💡 جاري المحاولة بنموذج بديل...")
    try:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        print("✅ تم تحميل النموذج البديل")
    except:
        print("❌ فشل تحميل نماذج Embeddings. البحث الدلالي غير متاح.")

# ========================= دوال مساعدة =========================

def remove_arabic_diacritics(text):
    """إزالة التشكيل والألف الخنجرية من النص العربي"""
    if not text:
        return ""
    # إزالة التشكيل
    text = re.sub(r'[\u064b-\u0652\u0670]', '', text)
    # إزالة الألف الخنجرية
    text = text.replace('\u0670', '')
    return text.strip()

def normalize_arabic_text(text):
    """تطبيع النص العربي (توحيد الهمزات والألفات)"""
    if not text:
        return ""

    # توحيد الهمزات
    text = re.sub('[إأآا]', 'ا', text)
    text = re.sub('ى', 'ي', text)
    text = re.sub('ة', 'ه', text)

    # إزالة التشكيل
    text = remove_arabic_diacritics(text)

    return text

def get_embedding(text, normalize=True):
    """توليد embedding للنص"""
    if model is None:
        return []
    if not text:
        return []

    try:
        # معالجة النص
        if normalize:
            text = normalize_arabic_text(text)
        text = text.replace("\n", " ").strip()

        # توليد embedding
        embedding = model.encode(text, normalize_embeddings=True)
        return embedding.tolist()
    except Exception as e:
        print(f"⚠️ خطأ في توليد embedding: {str(e)}")
        return []

# ========================= إنشاء الفهرس =========================

def create_quran_index(delete_if_exists=True):
    """إنشاء فهرس Elasticsearch"""
    if es is None:
        print("⚠️ لا يمكن إنشاء الفهرس: لا يوجد اتصال.")
        return False

    try:
        # حذف الفهرس القديم إذا كان موجوداً
        if delete_if_exists and es.indices.exists(index=INDEX_NAME):
            es.indices.delete(index=INDEX_NAME)
            print(f"🔄 تم حذف الفهرس القديم '{INDEX_NAME}'.")

        # إنشاء الفهرس الجديد
        es.indices.create(index=INDEX_NAME, body=mappings)
        print(f"✅ تم إنشاء الفهرس '{INDEX_NAME}' بنجاح.")
        return True

    except Exception as e:
        print(f"⚠️ خطأ أثناء إنشاء الفهرس: {str(e)}")
        return False

# ========================= الفهرسة =========================

def index_quran_data(file_path="quran_data.csv", batch_size=500):
    """فهرسة بيانات القرآن مع progress bar"""
    if es is None:
        print("⚠️ لا يمكن فهرسة البيانات: لا يوجد اتصال.")
        return False

    if not os.path.exists(file_path):
        print(f"⚠️ الملف '{file_path}' غير موجود.")
        return False

    try:
        # قراءة البيانات
        data = pd.read_csv(file_path)
        total_verses = len(data)
        print(f"📚 جاري فهرسة {total_verses} آية...")

        actions = []
        processed = 0

        for idx, row in data.iterrows():
            doc_id = f"{row['sura']}-{row['aya']}"
            aya_text = str(row["text"])

            # إعداد الوثيقة
            source_doc = {
                "sura": int(row["sura"]),
                "aya": int(row["aya"]),
                "text": aya_text,
                "text_raw": remove_arabic_diacritics(aya_text),
                "embedding": get_embedding(aya_text)
            }

            # إضافة حقول اختيارية
            if "sura_name" in row and pd.notna(row["sura_name"]):
                source_doc["sura_name"] = str(row["sura_name"])
            if "translation_en" in row and pd.notna(row["translation_en"]):
                source_doc["translation_en"] = str(row["translation_en"])

            actions.append({
                "_index": INDEX_NAME,
                "_id": doc_id,
                "_source": source_doc
            })

            processed += 1

            # طباعة التقدم
            if processed % 100 == 0:
                progress = (processed / total_verses) * 100
                print(f"⏳ التقدم: {processed}/{total_verses} ({progress:.1f}%)")

            # إرسال دفعة
            if len(actions) >= batch_size:
                helpers.bulk(es, actions, chunk_size=batch_size)
                actions = []

        # إرسال الدفعة الأخيرة
        if actions:
            helpers.bulk(es, actions, chunk_size=batch_size)

        # تحديث الفهرس
        es.indices.refresh(index=INDEX_NAME)

        print(f"✅ تم فهرسة {total_verses} آية بنجاح!")
        return True

    except Exception as e:
        print(f"⚠️ خطأ أثناء الفهرسة: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

# ========================= دوال البحث =========================

def lexical_search(query, top_k=10, fields=None, fuzziness="AUTO"):
    """بحث لغوي محسّن"""
    if es is None:
        return []

    if fields is None:
        fields = ["text^2", "text.raw^1.5", "sura_name^1.2", "translation_en"]

    try:
        response = es.search(
            index=INDEX_NAME,
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": fields,
                        "fuzziness": fuzziness,
                        "type": "best_fields",
                        "operator": "or",
                        "minimum_should_match": "75%"
                    }
                },
                "size": top_k,
                "_source": ["sura", "aya", "text", "sura_name"]
            }
        )
        return response["hits"]["hits"]
    except Exception as e:
        print(f"⚠️ خطأ في البحث اللغوي: {str(e)}")
        return []

def semantic_search_knn(query, top_k=10, num_candidates=None):
    """بحث دلالي باستخدام kNN"""
    if es is None or model is None:
        return []

    if num_candidates is None:
        num_candidates = min(top_k * 10, 500)

    query_vec = get_embedding(query)
    if not query_vec:
        return []

    try:
        response = es.search(
            index=INDEX_NAME,
            knn={
                "field": "embedding",
                "query_vector": query_vec,
                "k": top_k,
                "num_candidates": num_candidates
            },
            size=top_k,
            _source=["sura", "aya", "text", "sura_name"]
        )
        return response["hits"]["hits"]
    except Exception as e:
        print(f"⚠️ خطأ في البحث الدلالي kNN: {str(e)}")
        # محاولة العودة إلى script_score
        return semantic_search_script_score(query, top_k)

def semantic_search_script_score(query, top_k=10):
    """بحث دلالي باستخدام script_score (احتياطي)"""
    if es is None or model is None:
        return []

    query_vec = get_embedding(query)
    if not query_vec:
        return []

    try:
        response = es.search(
            index=INDEX_NAME,
            body={
                "query": {
                    "script_score": {
                        "query": {"match_all": {}},
                        "script": {
                            "source": "cosineSimilarity(params.query_vec, 'embedding') + 1.0",
                            "params": {"query_vec": query_vec}
                        }
                    }
                },
                "size": top_k,
                "_source": ["sura", "aya", "text", "sura_name"]
            }
        )
        return response["hits"]["hits"]
    except Exception as e:
        print(f"⚠️ خطأ في البحث الدلالي script_score: {str(e)}")
        return []

def hybrid_search(query, top_k=10, lex_weight=0.5, sem_weight=0.5):
    """بحث هجين محسّن يجمع بين اللغوي والدلالي"""
    if es is None:
        return []

    # الحصول على نتائج كلا النوعين
    lexical_results = lexical_search(query, top_k=top_k * 2)

    if model is not None:
        semantic_results = semantic_search_knn(query, top_k=top_k * 2)
    else:
        semantic_results = []

    # دمج النتائج بناءً على الأوزان
    combined_scores = {}

    # إضافة نتائج البحث اللغوي
    for hit in lexical_results:
        doc_id = hit['_id']
        score = hit['_score'] * lex_weight
        combined_scores[doc_id] = {
            'score': score,
            'hit': hit
        }

    # إضافة أو تحديث نتائج البحث الدلالي
    for hit in semantic_results:
        doc_id = hit['_id']
        score = hit['_score'] * sem_weight

        if doc_id in combined_scores:
            combined_scores[doc_id]['score'] += score
        else:
            combined_scores[doc_id] = {
                'score': score,
                'hit': hit
            }

    # ترتيب وإرجاع أفضل النتائج
    sorted_results = sorted(
        combined_scores.items(),
        key=lambda x: x[1]['score'],
        reverse=True
    )[:top_k]

    # إعادة تنسيق النتائج
    final_results = []
    for doc_id, data in sorted_results:
        hit = data['hit'].copy()
        hit['_score'] = data['score']
        final_results.append(hit)

    return final_results

# ========================= دوال إضافية =========================

def search_by_sura(sura_number, top_k=50):
    """البحث في سورة معينة"""
    if es is None:
        return []

    try:
        response = es.search(
            index=INDEX_NAME,
            body={
                "query": {
                    "term": {"sura": sura_number}
                },
                "sort": [{"aya": "asc"}],
                "size": top_k
            }
        )
        return response["hits"]["hits"]
    except Exception as e:
        print(f"⚠️ خطأ في البحث بالسورة: {str(e)}")
        return []

def get_verse(sura, aya):
    """الحصول على آية محددة"""
    if es is None:
        return None

    doc_id = f"{sura}-{aya}"
    try:
        response = es.get(index=INDEX_NAME, id=doc_id)
        return response['_source']
    except:
        return None

def get_index_stats():
    """الحصول على إحصائيات الفهرس"""
    if es is None:
        return None

    try:
        count = es.count(index=INDEX_NAME)
        stats = es.indices.stats(index=INDEX_NAME)

        return {
            'total_verses': count['count'],
            'index_size': stats['indices'][INDEX_NAME]['total']['store']['size_in_bytes'],
            'index_name': INDEX_NAME
        }
    except Exception as e:
        print(f"⚠️ خطأ في الحصول على الإحصائيات: {str(e)}")
        return None
