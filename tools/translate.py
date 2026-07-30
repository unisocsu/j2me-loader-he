import os
import requests

def main():
    token = os.environ.get("GH_MODEL_TOKEN")
    if not token:
        print("❌ לא נמצא טוקן גישה במשתני הסביבה!")
        exit(1)

    api_url = "https://models.inference.ai.azure.com/chat/completions"
    file_path = "app/src/main/res/values/strings.xml"

    if not os.path.exists(file_path):
        print(f"❌ קובץ המקור לא נמצא בנתיב: {file_path}")
        exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    print("⏳ שולח את קובץ ה-strings.xml לתרגום דרך ה-API...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    אתה עוזר פיתוח מומחה. לפניך תוכן של קובץ מחרוזות מאפליקציית אנדרואיד.
    אנא תרגם את כל המחרוזות לשפה העברית, שמור על מבנה ה-XML והתגיות בדיוק כפי שהם, ואל תמחק מחרוזות קיימות.
    החזר אך ורק את קובץ ה-XML המתורגם במלואו ללא שום טקסט או הסברים מסביב.

    תוכן הקובץ:
    {content}
    """

    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a professional software localization assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        result_data = response.json()
        translated_content = result_data["choices"][0]["message"]["content"]
        
        os.makedirs("app/src/main/res/values-he", exist_ok=True)
        output_path = "app/src/main/res/values-he/strings.xml"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(translated_content)
            
        print(f"✅ התרגום הושלם בהצלחה ונשמר בנתיב: {output_path}")
        
    except Exception as e:
        print(f"❌ אירעה שגיאה בתקשורת מול ה-API: {e}")
        exit(1)

if __name__ == "__main__":
    main()
