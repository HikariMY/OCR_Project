import tkinter as tk
from tkinter import font
from PIL import ImageGrab
import keyboard
import threading
from utils.ocr_translate import perform_ocr_and_translate

def retranslate(source_text, target_box):
    result = perform_ocr_and_translate(source_text)
    target_box.config(state="normal")
    target_box.delete("1.0", tk.END)
    target_box.insert(tk.END, result)
    target_box.config(state="disabled")

def capture_and_translate():
    root = tk.Tk()
    root.withdraw()

    selector = tk.Toplevel()
    selector.attributes("-fullscreen", True)
    selector.attributes("-alpha", 0.3)
    selector.attributes("-topmost", True)
    selector.config(bg="gray")

    canvas = tk.Canvas(selector, cursor="cross", bg="gray")
    canvas.pack(fill="both", expand=True)

    rect = None
    start_x = start_y = 0

    def on_mouse_down(event):
        nonlocal start_x, start_y, rect
        start_x, start_y = event.x, event.y
        rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red", width=2)

    def on_mouse_drag(event):
        canvas.coords(rect, start_x, start_y, event.x, event.y)

    def on_mouse_up(event):
        end_x, end_y = event.x, event.y
        selector.destroy()

        abs_start_x = selector.winfo_rootx() + start_x
        abs_start_y = selector.winfo_rooty() + start_y
        abs_end_x = selector.winfo_rootx() + end_x
        abs_end_y = selector.winfo_rooty() + end_y

        bbox = (min(abs_start_x, abs_end_x), min(abs_start_y, abs_end_y),
                max(abs_start_x, abs_end_x), max(abs_start_y, abs_end_y))

        image = ImageGrab.grab(bbox)
        original_text, translated_text = perform_ocr_and_translate(image, return_both=True)

        show_result(original_text, translated_text)

    canvas.bind("<Button-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    selector.mainloop()

def show_result(original, translated):
    win = tk.Toplevel()
    win.title("OCR Translate Result")
    win.geometry("600x400")

    fnt = font.Font(family="Arial", size=16)

    original_box = tk.Text(win, height=5, font=fnt)
    original_box.pack(fill="both", expand=False)
    original_box.insert("1.0", original)
    original_box.config(state="disabled")

    translated_box = tk.Text(win, height=10, font=fnt)
    translated_box.pack(fill="both", expand=True)
    translated_box.insert("1.0", translated)
    translated_box.config(state="disabled")

    bottom_frame = tk.Frame(win)
    bottom_frame.pack(fill="x")

    def on_retranslate():
        retranslate(original, translated_box)

    tk.Button(bottom_frame, text="Re-translate", command=on_retranslate).pack(side="right", padx=5, pady=5)
    tk.Button(bottom_frame, text="OK", command=win.destroy).pack(side="right", padx=5)

def hotkey_listener():
    print("📣 รอฟัง Ctrl+Alt+T เพื่อแปลภาพ")
    keyboard.add_hotkey("ctrl+alt+t", capture_and_translate)
    keyboard.wait()

if __name__ == "__main__":
    threading.Thread(target=hotkey_listener).start()
