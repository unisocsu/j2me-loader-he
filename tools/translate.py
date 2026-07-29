import json
import os

def get_keys_recursive(data, parent_key=''):
    """פונקציה רקורסיבית לשליפת כל המפתחות המקוננים מתוך קובץ JSON"""
    keys = set()
    for k, v in data.items():
        full_key = f"{parent_key}.{k}" if parent_key else k
        if isinstance(v, dict):
            keys.update(get_keys_recursive(v, full_key))
        else:
            keys.add(full_key)
    return keys

def check_missing_translations(base_file, target_file):
    """משווה בין קובץ מקור לקובץ יעד ומציג מה חסר"""
    if not os.path.exists(base_file):
        print(f"❌ קובץ המקור לא נמצא: {base_file}")
        return
    
    if not os.path.exists(target_file):
        print(f"❌ קובץ היעד לא נמצא: {target_file}")
        return

    with open(base_file, 'r', encoding='utf-8') as f:
        base_data = json.load(f)

    with open(target_file, 'r', encoding='utf-8') as f:
        target_data = json.load(f)

    base_keys = get_keys_recursive(base_data)
    target_keys = get_keys_recursive(target_data)

    missing_keys = base_keys - target_keys

    print(f"📊 תוצאות בדיקת תרגום עבור: {target_file}")
    print(סה"כ מפתחות במקור: {len(base_keys)}")
    print(f"✅ מפתחות קיימים ביעד: {len(target_keys)}")
    
    if missing_keys:
        print(f"⚠️ נמצאו {len(missing_keys)} מפתחות שדורשים תרגום:")
        for key in sorted(missing_keys):
            print(f"   🔹 {key}")
    else:
        print("🎉 כל המפתחות מתורגמים כהלכה! אין שום דבר חסר.")

if __name__ == "__main__":
    # הגדר כאן את נתיבי הקבצים שלך בפרויקט
    BASE_TRANSLATION_FILE = "locales/en.json"  # קובץ הבסיס (למשל אנגלית)
    TARGET_TRANSLATION_FILE = "locales/he.json"  # קובץ היעד לבדיקה (למשל עברית)

    check_missing_translations(BASE_TRANSLATION_FILE, TARGET_TRANSLATION_FILE)
