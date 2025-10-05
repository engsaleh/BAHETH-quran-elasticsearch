"""
ملف إعدادات التطبيق
يحتوي على جميع الإعدادات القابلة للتخصيص
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """إعدادات أساسية للتطبيق"""

    # إعدادات Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    TESTING = False
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False

    # إعدادات Elasticsearch
    ES_URL = os.getenv('ES_URL', 'https://localhost:9200')
    ES_USER = os.getenv('ES_USER', 'elastic')
    ES_PASS = os.getenv('ES_PASS', '')
    ES_INDEX = os.getenv('ES_INDEX', 'quran_search_v1')
    ES_TIMEOUT = int(os.getenv('ES_TIMEOUT', '30'))
    ES_MAX_RETRIES = int(os.getenv('ES_MAX_RETRIES', '3'))

    # إعدادات البحث
    DEFAULT_SEARCH_TYPE = 'hybrid'
    DEFAULT_TOP_K = 10
    MAX_TOP_K = 100
    MIN_TOP_K = 1

    # إعدادات نموذج Embeddings
    EMBEDDING_MODEL = os.getenv(
        'EMBEDDING_MODEL',
        'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    )
    EMBEDDING_DIM = int(os.getenv('EMBEDDING_DIM', '384'))

    # إعدادات البحث الهجين
    HYBRID_LEX_WEIGHT = float(os.getenv('HYBRID_LEX_WEIGHT', '0.5'))
    HYBRID_SEM_WEIGHT = float(os.getenv('HYBRID_SEM_WEIGHT', '0.5'))

    # إعدادات الأداء
    BULK_CHUNK_SIZE = int(os.getenv('BULK_CHUNK_SIZE', '500'))
    KNN_NUM_CANDIDATES = int(os.getenv('KNN_NUM_CANDIDATES', '100'))

    # مسارات الملفات
    DATA_DIR = os.getenv('DATA_DIR', 'data')
    QURAN_CSV = os.getenv('QURAN_CSV', 'quran_data.csv')
    QURAN_XML = os.getenv('QURAN_XML', 'data/quran-simple-plain.xml')

class DevelopmentConfig(Config):
    """إعدادات التطوير"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """إعدادات الإنتاج"""
    DEBUG = False
    TESTING = False
    # في الإنتاج، يجب استخدام متغيرات بيئة حقيقية

class TestingConfig(Config):
    """إعدادات الاختبار"""
    DEBUG = True
    TESTING = True
    ES_INDEX = 'quran_search_test'

# اختيار الإعدادات بناءً على البيئة
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """الحصول على الإعدادات الحالية"""
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)
