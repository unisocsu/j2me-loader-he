import os
import requests

def main():
    # הטוקן שלך מבוסס ה-AQ 🔑
    token = "AQ.Ab8RN6IsTBj1dL9wG1cTJIaWzTigqshC3m8VnNtCamOXg_8mwQ"
    
    file_path = "app/src/main/res/values/strings.xml"

    if not os.path.exists(file_path):
        print(f"❌ קובץ המקור לא נמצא בנתיב: {file_path}")
        exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    print("⏳ שולח את קובץ ה-strings.xml לתרגום דרך ה-API עם טוקן OAuth... 🤖")

    # כתובת ה-API המעודכנת למודלי Gemini
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    prompt = f"""
    אתה עוזר פיתוח מומחה. לפניך תוכן של קובץ מחרוזות מאפליקציית אנדרואיד.
    אנא תרגם את כל המחרוזות לשפה העברית, שמור על מבנה ה-XML והתגיות בדיוק כפי שהם, ואל תמחק מחרוזות קיימות.
    החזר אך ורק את קובץ ה-XML המתורגם במלואו ללא שום טקסט, מרכאות מעטפת או הסברים מסביב.

    תוכן הקובץ:
    {content}
    """

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result_data = response.json()
        
        # חילוץ התשובה מתוך מבנה ה-JSON של ה-API
        translated_content = result_data["candidates"][0]["content"]["parts"][0]["text"]
        
        # ניקוי מעטפות קוד במידה והמודל הוסיף אותן בטעות
        if translated_content.startswith("```xml"):
            translated_content = translated_content.lstrip("```xml").rstrip("```").strip()
        elif translated_content.startswith("```"):
            translated_content = translated_content.lstrip("```").rstrip("```").strip()

        os.makedirs("app/src/main/res/values-he", exist_ok=True)
        output_path = "app/src/main/res/values-he/strings.xml"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(translated_content)
            
        print(f"✅ התרגום הושלם בהצלחה ונשמר בנתיב: {output_path} 🎉")
        
    except Exception as e:
        print(f"❌ אירעה שגיאה בתקשורת מול ה-API: {e}")
        if 'response' in locals():
            print(f"פרטי שגיאה מהשרת: {response.text}")
        exit(1)

if __name__ == "__main__":
    main()
