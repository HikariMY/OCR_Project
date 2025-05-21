import tkinter as tk
from PIL import ImageGrab
import threading
import keyboard
from utils.ocr_translate import perform_ocr_and_translate

def show_overlay(text):
    overlay = tk.Tk()
    overlay.overrideredirect(True)
    overlay.attributes("-topmost", True)
    overlay.attributes("-alpha", 0.9)
    overlay.configure(bg="black")

    screen_width = overlay.winfo_screenwidth()
    screen_height = overlay.winfo_screenheight()

    width = 600
    height = 200
    x = (screen_width // 2) - (width // 2)
    y = 50

    overlay.geometry(f"{width}x{height}+{x}+{y}")

    label = tk.Label(overlay, text=text, font=("TH SarabunPSK", 18), fg="white", bg="black", wraplength=580, justify="left")
    label.pack(padx=10, pady=10)

    # ปิดเองอัตโนมัติหลัง 10 วินาที
    overlay.after(10000, overlay.destroy)
    overlay.mainloop()

def capture_and_translate():
    root = tk.Tk()
    root.withdraw()

    # หน้าจอลากแคป
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
        result = perform_ocr_and_translate(image)
        show_overlay(result)

    canvas.bind("<Button-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    selector.mainloop()

def hotkey_listener():
    print("📣 รอฟังคำสั่ง Ctrl+Alt+T เพื่อเริ่มแคปหน้าจอ...")
    keyboard.add_hotkey("ctrl+alt+t", capture_and_translate)
    keyboard.wait()  # รอไปเรื่อยๆ

if __name__ == "__main__":
    threading.Thread(target=hotkey_listener).start()
