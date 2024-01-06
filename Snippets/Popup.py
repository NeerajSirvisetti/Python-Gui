from tkinter import messagebox
import tkinter as tk

# Create a main window
window = tk.Tk()
window.title("GUI with Tkinter")

# Frame widget
frame1 = tk.Frame(window)
frame1.pack()

# Label widget in Frame
label_frame1 = tk.Label(frame1, text="Frame 1 Label")
label_frame1.pack()

# Another Frame with a Button
frame2 = tk.Frame(window)
frame2.pack()

button_frame2 = tk.Button(frame2, text="Click me in Frame 2")
button_frame2.grid(row=0, column=0)

# Using grid
label_frame1.grid(row=0, column=0)

# Create and pack a Text widget
text_widget = tk.Text(window, height=3, width=30)
text_widget.insert(tk.END, "This is a Text widget.")
text_widget.pack()

# Pop-up Window
def show_popup():
    popup_window = tk.Toplevel(window)
    popup_window.title("Popup Window")

    popup_label = tk.Label(popup_window, text="This is a popup window.")
    popup_label.pack()

popup_button = tk.Button(window, text="Show Popup", command=show_popup)
popup_button.pack()

# Function to show an info message
def show_info_message():
    messagebox.showinfo("Info", "This is an information message.")

# Button to trigger info message
info_button = tk.Button(window, text="Show Info", command=show_info_message)
info_button.pack()

# Ask Yes/No Question within Frame
def ask_question():
    response = messagebox.askyesno("Question", "Do you want to proceed?")
    if response:
        print("User clicked Yes")
    else:
        print("User clicked No")

question_button = tk.Button(frame2, text="Ask Question", command=ask_question)
question_button.grid(row=1, column=0)  # Use grid for the button within frame2

# Run the Tkinter event loop
window.mainloop()
