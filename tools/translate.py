import os
import re
import xml.etree.ElementTree as ET
from deep_translator import GoogleTranslator

# מונחים טכניים שלא נרצה לתרגם מילולית 🛑
PROTECTED_TERMS = [
    "MIDlet", "MIDP", "CLDC", "J2ME", "FPS", "RMS", "RecordStore", 
    "Canvas", "D-Pad", "Softkey", "JAR", "JAD", "Bluetooth", "Wi-Fi"
]

def protect_text(text):
    """מחליף משתנים ומונחים שמורים בטוקנים ניטרליים לפני השליחה לתרגום 🛡️"""
    replacements = {}
    counter = 0

    # 1. הגנה על משתני פורמט באנדרואיד (%1$s, %d, \n וכו')
    pattern_vars = r'(%\d+\$[a-zA-Z]|%[a-zA-Z]|\\[nrt])'
    for match in re.finditer(pattern_vars, text):
        val = match.group(0)
        token = f"__VAR_{counter}__"
        replacements[token] = val
        text = text.replace(val, token, 1)
        counter += 1

    # 2. הגנה על מונחים טכניים שמורים
    for term in PROTECTED_TERMS:
        if term in text:
            token = f"__TERM_{counter}__"
            replacements[token] = term
            text = text.replace(term, token)
            counter += 1

    return text, replacements

def restore_text(text, replacements):
    """מחזיר את המשתנים והמונחים המקוריים למקומם המדויק 🔄"""
    for token, original in replacements.items():
        text = text.replace(token, original)
    return text

def translate_node(elem, translator):
    """מתרגם אלמנט XML מדפיס את המקור והתוצאה ל-Logs 🔤📢"""
    if elem.attrib.get('translatable') == 'false':
        return

    if elem.text and elem.text.strip():
        original_text = elem.text
        protected_text, replacements = protect_text(original_text)
        try:
            translated = translator.translate(protected_text)
            restored = restore_text(translated, replacements)
            elem.text = restored
            
            # הדפסת התהליך ללוג של GitHub Actions 🖥️✨
            print(f"  ├─ 🔤 מקור:   '{original_text.strip()}'")
            print(f"  └─ 🎯 תרגום: '{restored}'\n")
        except Exception as e:
            print(f"⚠️ שגיאה בתרגום הטקסט '{original_text}': {e}\n")

def translate_xml_file(input_path, output_path, translator):
    """סורק ומתרגם קובץ XML יחיד מכל סוג (strings, arrays, plurals) 📄"""
    try:
        tree = ET.parse(input_path)
        root = tree.getroot()
    except Exception as e:
        print(f"⚠️ לא ניתן לפענח את הקובץ {input_path}: {e}")
        return

    filename = os.path.basename(input_path)
    print(f"==================================================")
    print(f"🚀 מתחיל לתרגם את הקובץ: {filename}")
    print(f"==================================================")

    # תרגום מחרוזות רגילות <string>
    for elem in root.findall('string'):
        translate_node(elem, translator)

    # תרגום מערכים <string-array>
    for array_elem in root.findall('string-array'):
        if array_elem.attrib.get('translatable') == 'false':
            continue
        for item in array_elem.findall('item'):
            translate_node(item, translator)

    # תרגום ביטויי ריבוי <plurals>
    for plurals_elem in root.findall('plurals'):
        if plurals_elem.attrib.get('translatable') == 'false':
            continue
        for item in plurals_elem.findall('item'):
            translate_node(item, translator)

    # שמירת הקובץ המתורגם בתיקיית היעד values-he
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"✅ הקובץ {filename} תורגם ונשמר בהצלחה בנתיב: {output_path}\n")

def main():
    translator = GoogleTranslator(source='auto', target='iw')
    
    base_dir = "app/src/main/res"
    values_dir = os.path.join(base_dir, "values")
    target_dir = os.path.join(base_dir, "values-he")

    if not os.path.exists(values_dir):
        print(f"❌ התיקייה לא נמצאה: {values_dir}")
        return

    # סריקת כל קובצי ה-XML בתיקיית values 🗂️
    xml_files = [f for f in os.listdir(values_dir) if f.endswith('.xml')]
    print(f"🔍 נמצאו {len(xml_files)} קובצי XML בתיקיית values.\n")

    for filename in xml_files:
        input_file = os.path.join(values_dir, filename)
        output_file = os.path.join(target_dir, filename)
        translate_xml_file(input_file, output_file, translator)

if __name__ == "__main__":
    main()
