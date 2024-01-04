import tkinter as tk
from tkinter import ttk

def on_dropdown_select(event):
    selected_value = dropdown_var.get()
    print(f"Selected: {selected_value}")

# Create the main window
root = tk.Tk()
root.title("Custom Dropdown Color")

# Create a style object
style = ttk.Style()

# Set the background color of the dropdown list
style.configure('TCombobox', fieldbackground='blue')
style.map('TCombobox', fieldbackground=[('readonly','green')])

# List of options for the dropdown
options = ["Init", "Floorplan", "Powerplan", "Place", "PreCts", "Cts", "PostCts", "Route", "PostRoute"]

# Create a variable to store the selected value
dropdown_var = tk.StringVar()

# Create the dropdown widget
dropdown = ttk.Combobox(root, values=options, textvariable=dropdown_var, state="readonly")
dropdown.bind("<<ComboboxSelected>>", on_dropdown_select)
dropdown.pack(pady=20)

# Run the main loop
root.mainloop()