"""
تطبيق Flask للبحث في القرآن الكريم
يدعم البحث اللغوي والدلالي والهجين مع واجهة ويب حديثة
 م.علا صالح
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
# استيراد وظائف البحث من الملف الخلفي
import quran_search_backend as quran_es

# تحميل المتغيرات البيئية
load_dotenv()

# إنشاء تطبيق Flask
app = Flask(__name__)
CORS(app)  # للسماح بطلبات AJAX

# إعدادات التطبيق
app.config['JSON_AS_ASCII'] = False  # لدعم النصوص العربية
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    """
    نقطة نهاية API للبحث
    يقبل JSON بالشكل:
    {
        "query": "نص البحث",
        "search_type": "lexical|semantic|hybrid",
        "top_k": 10
    }
    """
    try:
        # التحقق من الاتصال بـ Elasticsearch
        if quran_es.es is None or not quran_es.es.ping():
            return jsonify({
                'success': False,
                'error': 'فشل الاتصال بقاعدة البيانات. يرجى المحاولة لاحقاً.'
            }), 503

        # الحصول على البيانات من الطلب
        data = request.get_json()

        query = data.get('query', '').strip()
        search_type = data.get('search_type', 'hybrid')
        top_k = int(data.get('top_k', 10))

        # التحقق من صحة المدخلات
        if not query:
            return jsonify({
                'success': False,
                'error': 'الرجاء إدخال نص للبحث'
            }), 400

        if top_k <= 0 or top_k > 100:
            top_k = 10

        # تنفيذ البحث بناءً على النوع
        results = []
        if search_type == 'lexical':
            results = quran_es.lexical_search(query, top_k=top_k)
        elif search_type == 'semantic':
            results = quran_es.semantic_search_knn(query, top_k=top_k)
        else:  # hybrid
            results = quran_es.hybrid_search(query, top_k=top_k)

        # تنسيق النتائج
        formatted_results = []
        for hit in results:
            source = hit['_source']
            formatted_results.append({
                'sura': source.get('sura'),
                'aya': source.get('aya'),
                'text': source.get('text'),
                'sura_name': source.get('sura_name', 'غير معروفة'),
                'score': round(hit['_score'], 3)
            })

        return jsonify({
            'success': True,
            'results': formatted_results,
            'count': len(formatted_results),
            'query': query,
            'search_type': search_type
        })

    except ValueError as ve:
        return jsonify({
            'success': False,
            'error': f'خطأ في البيانات المدخلة: {str(ve)}'
        }), 400

    except Exception as e:
        print(f"خطأ في البحث: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'حدث خطأ أثناء البحث. يرجى المحاولة مرة أخرى.'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """التحقق من حالة الخدمة"""
    try:
        es_status = quran_es.es is not None and quran_es.es.ping()
        model_status = quran_es.model is not None

        return jsonify({
            'status': 'healthy' if es_status else 'degraded',
            'elasticsearch': es_status,
            'embedding_model': model_status,
            'index_name': quran_es.INDEX_NAME
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """إحصائيات عن الفهرس"""
    try:
        if quran_es.es is None:
            return jsonify({'error': 'لا يوجد اتصال بقاعدة البيانات'}), 503

        # الحصول على عدد الوثائق
        count = quran_es.es.count(index=quran_es.INDEX_NAME)

        return jsonify({
            'success': True,
            'total_verses': count['count'],
            'index_name': quran_es.INDEX_NAME
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """معالج الصفحات غير الموجودة"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """معالج أخطاء الخادم"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # التحقق من الاتصال عند بدء التطبيق
    print("\n" + "="*60)
    print(" بدء تشغيل تطبيق البحث في القرآن الكريم")
    print("="*60)

    if quran_es.es is not None and quran_es.es.ping():
        print(" الاتصال بـ Elasticsearch ناجح")
        try:
            count = quran_es.es.count(index=quran_es.INDEX_NAME)
            print(f" عدد الآيات في الفهرس: {count['count']}")
        except:
            print(" الفهرس غير موجود. قم بتشغيل setup_index.py")
    else:
        print(" فشل الاتصال بـ Elasticsearch")
        print(" تأكد من تشغيل Elasticsearch وصحة الإعدادات في .env")

    if quran_es.model is not None:
        print(" نموذج Embeddings جاهز")
    else:
        print(" نموذج Embeddings غير متاح")

    print("\n التطبيق يعمل على: http://127.0.0.1:5000")
    print("="*60 + "\n")

    # تشغيل التطبيق
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )
