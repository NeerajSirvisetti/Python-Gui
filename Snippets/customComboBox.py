import tkinter as tk
from tkinter import ttk

class CustomComboboxStyle:
    def __init__(self, combobox):
        self.combobox = combobox
        self.selected_bg_color = "green"
        self.normal_bg_color = "white"

        # Configure the style
        self.style = ttk.Style()
        self.style.configure("Custom.TCombobox", padding=5, fieldbackground=self.normal_bg_color)

        # Set up event bindings
        self.combobox.bind("<FocusIn>", self.on_combobox_focus)
        self.combobox.bind("<FocusOut>", self.on_combobox_focus_out)

    def on_combobox_focus(self, event):
        self.style.configure("Custom.TCombobox", fieldbackground="green")

    def on_combobox_focus_out(self, event):
        self.style.configure("Custom.TCombobox", fieldbackground="white")

# Create the main window
root = tk.Tk()
root.title("Custom Combobox Style")

# Create a Combobox
combo_values = ["Option1", "Option2", "Option3"]
selected_value = tk.StringVar()
combobox = ttk.Combobox(root, textvariable=selected_value, values=combo_values, style="Custom.TCombobox")
combobox.pack(pady=10, padx=10)

# Create an instance of the custom style
custom_style = CustomComboboxStyle(combobox)

# Run the main loop
root.mainloop()
