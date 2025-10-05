#!/usr/bin/env python3
"""
سكريبت لاختبار وظائف البحث
يمكن استخدامه للتأكد من عمل جميع أنواع البحث بشكل صحيح
"""

import quran_search_backend as quran_es
import sys

def print_results(results, search_type):
    """طباعة نتائج البحث بشكل منسق"""
    print(f"\n{'='*70}")
    print(f"نتائج البحث {search_type}")
    print('='*70)

    if not results:
        print(" لم يتم العثور على نتائج")
        return

    for i, hit in enumerate(results, 1):
        src = hit['_source']
        score = hit['_score']

        print(f"\n{i}. سورة {src.get('sura_name', 'غير معروفة')} ({src['sura']}:{src['aya']})")
        print(f"   النص: {src['text']}")
        print(f"   الدقة: {score:.3f}")

    print('\n' + '='*70)

def test_connection():
    """اختبار الاتصال بـ Elasticsearch"""
    print("\n🔍 اختبار الاتصال بـ Elasticsearch...")

    if quran_es.es is None:
        print(" فشل: لا يوجد كائن Elasticsearch")
        return False

    try:
        if not quran_es.es.ping():
            print(" فشل: لا يمكن الاتصال بـ Elasticsearch")
            return False

        print(" نجح: الاتصال بـ Elasticsearch")

        # التحقق من وجود الفهرس
        if not quran_es.es.indices.exists(index=quran_es.INDEX_NAME):
            print(f"  تحذير: الفهرس '{quran_es.INDEX_NAME}' غير موجود")
            print("   قم بتشغيل: python setup_index.py")
            return False

        # عرض عدد الوثائق
        count = quran_es.es.count(index=quran_es.INDEX_NAME)
        print(f" عدد الآيات في الفهرس: {count['count']}")

        return True

    except Exception as e:
        print(f" خطأ: {str(e)}")
        return False

def test_lexical_search(query="الصلاة", top_k=5):
    """اختبار البحث اللغوي"""
    print(f"\n اختبار البحث اللغوي: '{query}'")

    try:
        results = quran_es.lexical_search(query, top_k=top_k)
        print_results(results, "اللغوي")
        return len(results) > 0
    except Exception as e:
        print(f" فشل البحث اللغوي: {str(e)}")
        return False

def test_semantic_search(query="الصبر على المحن", top_k=5):
    """اختبار البحث الدلالي"""
    print(f"\n اختبار البحث الدلالي: '{query}'")

    if quran_es.model is None:
        print("  تحذير: نموذج Embeddings غير متاح")
        return False

    try:
        results = quran_es.semantic_search_knn(query, top_k=top_k)
        print_results(results, "الدلالي")
        return len(results) > 0
    except Exception as e:
        print(f" فشل البحث الدلالي: {str(e)}")
        return False

def test_hybrid_search(query="الرحمة", top_k=5):
    """اختبار البحث الهجين"""
    print(f"\n اختبار البحث الهجين: '{query}'")

    try:
        results = quran_es.hybrid_search(query, top_k=top_k)
        print_results(results, "الهجين")
        return len(results) > 0
    except Exception as e:
        print(f" فشل البحث الهجين: {str(e)}")
        return False

def run_all_tests():
    """تشغيل جميع الاختبارات"""
    print("\n" + "="*70)
    print(" بدء اختبارات البحث في القرآن الكريم")
    print("="*70)

    # اختبار الاتصال
    if not test_connection():
        print("\n فشل اختبار الاتصال. لا يمكن متابعة الاختبارات.")
        sys.exit(1)

    # تشغيل الاختبارات
    tests_passed = 0
    tests_total = 3

    if test_lexical_search():
        tests_passed += 1

    if test_semantic_search():
        tests_passed += 1

    if test_hybrid_search():
        tests_passed += 1

    # النتيجة النهائية
    print("\n" + "="*70)
    print(f" النتيجة: نجح {tests_passed} من {tests_total} اختبار")
    print("="*70)

    if tests_passed == tests_total:
        print(" جميع الاختبارات نجحت! النظام يعمل بشكل صحيح.")
        return True
    else:
        print(f"  فشل {tests_total - tests_passed} اختبار. يرجى مراجعة الأخطاء أعلاه.")
        return False

def interactive_search():
    """وضع البحث التفاعلي"""
    print("\n" + "="*70)
    print(" وضع البحث التفاعلي")
    print("="*70)
    print("أدخل استعلام بحث (أو 'exit' للخروج)")

    while True:
        print("\n" + "-"*70)
        query = input(" البحث: ").strip()

        if query.lower() in ['exit', 'quit', 'خروج']:
            print(" وداعاً!")
            break

        if not query:
            continue

        print("\nاختر نوع البحث:")
        print("1. لغوي (Lexical)")
        print("2. دلالي (Semantic)")
        print("3. هجين (Hybrid) - موصى به")

        choice = input("الاختيار (1/2/3) [3]: ").strip() or "3"

        top_k = input("عدد النتائج [5]: ").strip() or "5"
        try:
            top_k = int(top_k)
        except:
            top_k = 5

        try:
            if choice == "1":
                results = quran_es.lexical_search(query, top_k=top_k)
                print_results(results, "اللغوي")
            elif choice == "2":
                results = quran_es.semantic_search_knn(query, top_k=top_k)
                print_results(results, "الدلالي")
            else:
                results = quran_es.hybrid_search(query, top_k=top_k)
                print_results(results, "الهجين")
        except Exception as e:
            print(f" خطأ في البحث: {str(e)}")

def main():
    """الوظيفة الرئيسية"""
    import argparse

    parser = argparse.ArgumentParser(
        description='اختبار وظائف البحث في القرآن الكريم'
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='تشغيل الوضع التفاعلي'
    )
    parser.add_argument(
        '--query', '-q',
        type=str,
        help='استعلام بحث مباشر'
    )
    parser.add_argument(
        '--type', '-t',
        choices=['lexical', 'semantic', 'hybrid'],
        default='hybrid',
        help='نوع البحث'
    )
    parser.add_argument(
        '--top-k', '-k',
        type=int,
        default=5,
        help='عدد النتائج'
    )

    args = parser.parse_args()

    # التحقق من الاتصال أولاً
    if not test_connection():
        sys.exit(1)

    if args.interactive:
        interactive_search()
    elif args.query:
        print(f"\n البحث عن: '{args.query}'")
        if args.type == 'lexical':
            results = quran_es.lexical_search(args.query, top_k=args.top_k)
            print_results(results, "اللغوي")
        elif args.type == 'semantic':
            results = quran_es.semantic_search_knn(args.query, top_k=args.top_k)
            print_results(results, "الدلالي")
        else:
            results = quran_es.hybrid_search(args.query, top_k=args.top_k)
            print_results(results, "الهجين")
    else:
        run_all_tests()

if __name__ == "__main__":
    main()
