from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\asus\AppData\Local\Programs\Tesseract-OCR"
from deep_translator import GoogleTranslator

def perform_ocr_and_translate(image: Image.Image) -> str:
    # OCR ด้วยภาษาอังกฤษ
    text = pytesseract.image_to_string(image, lang='eng')

    # แปลจากอังกฤษ → ไทย
    try:
        translated = GoogleTranslator(source='en', target='th').translate(text)
    except Exception as e:
        translated = f"เกิดข้อผิดพลาดในการแปล: {e}"

    return translated
