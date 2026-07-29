from deep_translator import GoogleTranslator

def test_translation():
    word_to_translate = "Hello world"
    print(f"שולח לבדיקה את המילה: '{word_to_translate}'...")
    
    try:
        result = GoogleTranslator(source='en', target='he').translate(word_to_translate)
        print(f"תשובה מהמתרגם: '{result}'")
    except Exception as e:
        print(f"שגיאה בזמן התרגום: {e}")

if __name__ == "__main__":
    test_translation()
