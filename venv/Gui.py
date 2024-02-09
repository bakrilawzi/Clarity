import tkinter as tk
from tkinter import ttk

def create_rectangle_with_os_style_buttons(root, percentage_height):
    canvas = tk.Canvas(root, height=400, width=400)
    canvas.pack()

    # Calculate the height of the rectangle based on the percentage
    canvas_height = canvas.winfo_reqheight()
    rectangle_height = canvas_height * percentage_height

    # Create the blue rectangle with full width and calculated height
    canvas.create_rectangle(0, canvas_height - rectangle_height, canvas.winfo_reqwidth(), canvas_height, fill="black")

    # Create two circular buttons with native OS style
    style = ttk.Style()
    style.configure("TButton", padding=6)

    button_radius = min(canvas.winfo_reqwidth() // 8, rectangle_height // 2)

    button1 = ttk.Button(root, text="Button 1", style="TButton")
    button2 = ttk.Button(root, text="Button 2", style="TButton")

    # Place the circular buttons on the canvas
   
    canvas.create_window(canvas.winfo_reqwidth() // 4, canvas_height - rectangle_height // 2, anchor=tk.CENTER, window=button1)

   
    canvas.create_window(3 * canvas.winfo_reqwidth() // 4, canvas_height - rectangle_height // 2, anchor=tk.CENTER, window=button2)

    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
    create_rectangle_with_os_style_buttons(root, 0.2)
