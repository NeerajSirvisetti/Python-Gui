import tkinter as tk
from tkinter import ttk

def check_condition(option):
    # Replace this condition with your own logic
    return option.startswith("B")  # Change the condition as needed

root = tk.Tk()
root.title("Custom Colored Dropdown Options")

options = ["Apple", "Banana", "Orange", "Carrot", "Broccoli", "Spinach"]

# Create a custom style for the TCombobox
style = ttk.Style()

# Set the background color for each element based on the condition
for index, option in enumerate(options):
    if check_condition(option):
        style.configure(f"Custom.TCombobox.Option{index}", fieldbackground="lightgreen")
    else:
        style.configure(f"Custom.TCombobox.Option{index}", fieldbackground="lightcoral")

# Create the dropdown using a TCombobox
dropdown = ttk.Combobox(
    root,
    values=options,
    state="readonly",
    style="Custom.TCombobox",
)
dropdown.pack(pady=10)

root.mainloop()