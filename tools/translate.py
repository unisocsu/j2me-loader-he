import os
from google import genai

def main():
    # הדבק כאן את מפתח ה-API הנכון שמתחיל ב-AIzaSy... 🔑
    api_key = "AQ.Ab8RN6KmtcwtPXbGPInjwFthSpD3o075waYKOyj-DHygFJrKMQ"
    
    file_path = "app/src/main/res/values/strings.xml"

    if not os.path.exists(file_path):
        print(f"❌ קובץ המקור לא נמצא בנתיב: {file_path}")
        exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    print("⏳ שולח את קובץ ה-strings.xml לתרגום דרך Gemini API... 🤖")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    אתה עוזר פיתוח מומחה. לפניך תוכן של קובץ מחרוזות מאפליקציית אנדרואיד.
    אנא תרגם את כל המחרוזות לשפה העברית, שמור על מבנה ה-XML והתגיות בדיוק כפי שהם, ואל תמחק מחרוזות קיימות.
    החזר אך ורק את קובץ ה-XML המתורגם במלואו ללא שום טקסט, מרכאות מעטפת או הסברים מסביב.

    תוכן הקובץ:
    {content}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        translated_content = response.text
        
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
        print(f"❌ אירעה שגיאה בתקשורת מול ה-API של Gemini: {e}")
        exit(1)

if __name__ == "__main__":
    main()
