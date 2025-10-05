import xml.etree.ElementTree as ET
import pandas as pd
import re

def remove_arabic_diacritics(text):
    """إزالة التشكيل من النص العربي"""
    if not text:
        return ""
    return re.sub(r'[\u064b-\u0652\u0670]', '', text)

def generate_csv_from_xml(xml_file_path="data/quran-simple-plain.xml", output_csv_path="quran_data.csv"):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    records = []
    for sura in root.findall('sura'):
        sura_index = int(sura.get('index'))
        sura_name = sura.get('name')

        for aya in sura.findall('aya'):
            aya_index = int(aya.get('index'))
            text = aya.get('text')
            bismillah = aya.get('bismillah', '') # لالتقاط البسملة إذا كانت attribute منفصلة

            # هنا يمكنك إضافة منطق لدمج الترجمات، اللمات، إلخ.
            # حالياً، فقط النصوص الأساسية

            record = {
                "sura": sura_index,
                "aya": aya_index,
                "text": text,
                "sura_name": sura_name,
                # "text_no_diacritics": remove_arabic_diacritics(text), # يمكن إضافته هنا أو تركه لـ quran_search.py
                # "translation_en": "...", # هنا يمكن جلب الترجمة الإنجليزية
                # "lemma": "...", # هنا يمكن جلب الجذر اللغوي
                # "juz": "...",
                # "page": "..."
            }
            records.append(record)

    df = pd.DataFrame(records)
    df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    print(f"✅ تم إنشاء ملف CSV بنجاح في: {output_csv_path}")

if __name__ == "__main__":
    # تأكد من وجود مجلد data وملف quran-simple-plain.xml فيه
    # وإلا قد تحتاج لتعديل المسار
    generate_csv_from_xml()
