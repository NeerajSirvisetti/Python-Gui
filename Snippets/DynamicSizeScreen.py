import tkinter as tk
from tkinter import ttk

class DynamicSizeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Dynamic Size GUI")
        self.update_window_size()

    def update_window_size(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Set the window size based on a percentage of the screen dimensions
        width_percentage = 0.8
        height_percentage = 0.8
        window_width = int(screen_width * width_percentage)
        window_height = int(screen_height * height_percentage)

        # Calculate the x and y positions to center the window
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.master.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

def main():
    root = tk.Tk()
    app = DynamicSizeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()