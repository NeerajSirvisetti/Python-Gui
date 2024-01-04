import tkinter as tk
from tkinter import ttk


class CustomComboboxStyle:
    def __init__(self):
        self.style = ttk.Style()

        # Create a style for the dropdown list elements
        self.style.configure("Custom.TCombobox", padding=5, fieldbackground="white", readonlybackground="white")

        # Create a style for the dropdown label (when an option is selected)
        self.style.map("Custom.TCombobox", background=[('active', 'green')], readonlybackground=[('selected', 'green')])

# Create the main window
root = tk.Tk()
root.title("Custom Combobox Style")

# Create an instance of the custom style
custom_style = CustomComboboxStyle()

# Create a Combobox with the custom style
combo_values = ["Option1", "Option2", "Option3"]
selected_value = tk.StringVar()

combobox = ttk.Combobox(root, textvariable=selected_value, values=combo_values, style="Custom.TCombobox")
combobox.pack(pady=10, padx=10)

# Run the main loop
root.mainloop()