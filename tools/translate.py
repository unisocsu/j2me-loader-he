import os
import re

def scan_java_file(file_path):
    """סורק קובץ Java בודד ומחפש מחרוזות טקסט בתוך מרכאות 📄"""
    strings_found = []
    
    # ביטוי רגולרי לאיתור טקסט בתוך מרכאות כפולות, תוך התעלמות מאימפורטים, הערות או שורות ריקות
    # מתאים למחרוזות המכילות אותיות, רווחים וסימנים טיפוסיים לממשק משתמש
    string_pattern = r'"([^"\\]*(?:\\.[^"\\]*)*)"'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # דילוג על הערות בקוד או שורות ייבוא
            if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*') or stripped.startswith('import '):
                continue
                
            matches = re.findall(string_pattern, line)
            for match in matches:
                # סינון מחרוזות טכניות קצרות מדי או כאלה שאינן טקסט אנושי (כמו תגיות XML, שמות קבצים, או מפתחי URL)
                if len(match.strip()) > 1 and not match.startswith('android.') and not match.startswith('R.'):
                    strings_found.append((line_num, match))
                    
    except Exception as e:
        print(f"⚠️ שגיאה בקריאת הקובץ {file_path}: {e}")
        
    return strings_found

def main():
    # נתיב תיקיית הקוד בפרויקט אנדרואיד
    java_dir = "app/src/main/java"
    
    if not os.path.exists(java_dir):
        print(f"❌ התיקייה לא נמצאה: {java_dir}")
        return

    print(f"🔍 מתחיל לסרוק קובצי Java בנתיב: {java_dir}\n" + "="*50)

    total_files = 0
    total_strings = 0

    for root, dirs, files in os.walk(java_dir):
        for file in files:
            if file.endswith('.java'):
                total_files += 1
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, java_dir)
                
                strings = scan_java_file(full_path)
                if strings:
                    print(f"\n📂 קובץ: {rel_path}")
                    print(f"   מצאנו {len(strings)} מחרוזות פוטנציאליות לתרגום:")
                    for line_num, text in strings:
                        print(f"     [שורה {line_num}] ➔ \"{text}\"")
                        total_strings += 1

    print("\n" + "="*50)
    print(f"✅ סיום הסריקה! סה\"כ נסרקו {total_files} קובצי Java ונמצאו {total_strings} מחרוזות לסקירה.")

if __name__ == "__main__":
    main()
