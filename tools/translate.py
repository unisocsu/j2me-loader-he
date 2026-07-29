import os
import re

# הגדרת סיומות קבצי הקוד שנרצה לסרוק
CODE_EXTENSIONS = {'.java', '.kt', '.cpp', '.c', '.h', '.hpp'}

# ביטוי רגולרי לאיתור מחרוזות טקסט בתוך מרכאות כפולות ברוב השפות
STRING_LITERAL_REGEX = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"')

def should_skip_dir(dirname):
    """דילוג על תיקיות בנייה או מערכת מיותרות"""
    skipped = {'build', '.git', '.gradle', '.idea', 'node_modules', 'libs', 'prebuilt'}
    return dirname in skipped or dirname.startswith('.')

def analyze_code_file(file_path):
    """סורק קובץ קוד בודד ומחזיר רשימת מחרוזות טקסט ש נמצאו בו"""
    found_strings = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                # דילוג על שורות הערה פשוטות (אופציונלי)
                stripped = line.strip()
                if stripped.startswith('//') or stripped.startswith('*') or stripped.startswith('/*'):
                    continue
                
                matches = STRING_LITERAL_REGEX.findall(line)
                for text in matches:
                    # סינון מחרוזות ריקות, תווים בודדים, או מילות מפתח טכניות נפוצות
                    if len(text.strip()) > 1 and not text.startswith(('http://', 'https://', 'android.', 'java.', 'com.', 'Ljava', 'V', 'I', 'Z', '[')):
                        found_strings.append((line_num, text))
    except Exception as e:
        print(f"⚠️ שגיאה בקריאת הקובץ {file_path}: {e}")
        
    return found_strings

def scan_project_source_files():
    """סורק את כל הפרויקט מקצה לקצה ומציג טקסטים בקוד שדורשים בדיקה/תרגום"""
    project_root = '.'
    scanned_files_count = 0
    total_strings_found = 0
    
    print("🔎 מתחיל בסריקת קבצי הקוד בפרויקט (Java, Kotlin, C, C++)... 🚀\n")

    for root, dirs, files in os.walk(project_root):
        # סינון תיקיות
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in CODE_EXTENSIONS:
                file_path = os.path.join(root, file)
                scanned_files_count += 1
                
                strings = analyze_code_file(file_path)
                if strings:
                    print(f"📄 קובץ: {file_path}")
                    for line_num, text in strings:
                        print(f"   🔹 שורה {line_num}: \"{text}\"")
                        total_strings_found += 1
                    print("-" * 50)

    print(f"\n📊 סיכום סריקה:")
    print(f"📁 סך הכל קבצי קוד שנסרקו: {scanned_files_count}")
    print(f"⚠️ נמצאו בסך הכל {total_strings_found} מחרוזות טקסט קשיחות בקוד שדורשות בדיקה או תרגום.")

if __name__ == "__main__":
    scan_project_source_files()
