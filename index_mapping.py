# index_mapping.py
# تعريف بنية فهرس القرآن الكريم مع إعدادات تحليل لغوي عربي محسّنة

mappings = {
    "settings": {
        "analysis": {
            "analyzer": {
                "arabic_text_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "arabic_stop",
                        "arabic_normalization",
                        "arabic_stemmer_light"
                    ]
                },
                "arabic_keyword_analyzer": {
                    "type": "custom",
                    "tokenizer": "keyword",
                    "filter": ["arabic_normalization"]
                }
            },
            "filter": {
                "arabic_stop": {"type": "stop", "stopwords": "_arabic_"},
                "arabic_normalization": {"type": "arabic_normalization"},
                "arabic_stemmer_light": {
                    "type": "arabic_stem",
                    "stem_unigrams": False
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "sura": {"type": "integer"},
            "aya": {"type": "integer"},
            "sura_name": { # إضافة حقل لاسم السورة
                "type": "text",
                "analyzer": "arabic_keyword_analyzer" # يمكن البحث فيه بدقة أو ككلمة مفتاحية
            },
            "text": {
                "type": "text",
                "analyzer": "arabic_text_analyzer",
                "search_analyzer": "arabic_text_analyzer",
                "fields": {
                    "raw": { # حقل فرعي للنص كما هو (أو بتطبيع بسيط)
                        "type": "text",
                        "analyzer": "arabic_keyword_analyzer"
                    }
                }
            },
            "translation_en": {
                "type": "text",
                "analyzer": "standard", # استخدام المحلل القياسي للغة الإنجليزية
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "embedding": {"type": "dense_vector", "dims": 384, "index": True, "similarity": "cosine"}
            # يمكنك إضافة حقول أخرى هنا إذا كانت متوفرة في quran_data.csv
            # مثال: "juz": {"type": "integer"},
            # مثال: "page": {"type": "integer"},
            # مثال: "lemma": {"type": "text", "analyzer": "arabic_text_analyzer"},
        }
    }
}
