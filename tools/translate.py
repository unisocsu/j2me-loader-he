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

def translate_xml(input_path, output_path):
    # שימוש בקוד 'iw' המעודכן עבור עברית 🌍✨
    translator = GoogleTranslator(source='auto', target='iw')
    
    tree = ET.parse(input_path)
    root = tree.getroot()

    print(f"🚀 מתחיל לתרגם את הקובץ: {input_path}")

    # תרגום מחרוזות רגילות <string>
    for elem in root.findall('string'):
        if elem.attrib.get('translatable') == 'false':
            continue

        if elem.text and elem.text.strip():
            protected_text, replacements = protect_text(elem.text)
            try:
                translated = translator.translate(protected_text)
                elem.text = restore_text(translated, replacements)
            except Exception as e:
                print(f"⚠️ שגיאה בתרגום המחרוזת '{elem.attrib.get('name')}': {e}")

    # תרגום מערכים <string-array>
    for array_elem in root.findall('string-array'):
        if array_elem.attrib.get('translatable') == 'false':
            continue
            
        for item in array_elem.findall('item'):
            if item.text and item.text.strip():
                protected_text, replacements = protect_text(item.text)
                try:
                    translated = translator.translate(protected_text)
                    item.text = restore_text(translated, replacements)
                except Exception as e:
                    print(f"⚠️ שגיאה בתרגום פריט במערך: {e}")

    # שמירת הקובץ המתורגם בתיקייה
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"✅ התרגום הושלם בהצלחה! הקובץ שנשמר: {output_path}")

if __name__ == "__main__":
    # הגדרת נתיבי הקבצים בפרויקט 📁
    base_dir = "app/src/main/res"
    
    input_strings = os.path.join(base_dir, "values", "strings.xml")
    output_strings = os.path.join(base_dir, "values-he", "strings.xml")
    
    if os.path.exists(input_strings):
        translate_xml(input_strings, output_strings)
    else:
        print(f"❌ הקובץ לא נמצא: {input_strings}")
