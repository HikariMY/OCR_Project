import tkinter as tk
from tkinter import messagebox
import pyautogui
from utils.ocr_translate import perform_ocr_and_translate

def capture_and_translate():
    messagebox.showinfo("คำแนะนำ", "ลากเมาส์เพื่อเลือกพื้นที่ภาพ")
    screenshot = pyautogui.screenshot(region=pyautogui.selectRegion())  # ต้องใช้ lib เสริม
    result = perform_ocr_and_translate(screenshot)
    output_box.config(state='normal')
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result)
    output_box.config(state='disabled')

app = tk.Tk()
app.title("OCR Translator")
app.geometry("600x400")

button = tk.Button(app, text="แคปภาพและแปล", command=capture_and_translate, font=("TH SarabunPSK", 20))
button.pack(pady=20)

output_box = tk.Text(app, height=10, font=("TH SarabunPSK", 18))
output_box.pack(padx=10, pady=10)
output_box.config(state='disabled')

app.mainloop()
