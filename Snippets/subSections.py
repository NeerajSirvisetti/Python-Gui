import tkinter as tk

root = tk.Tk()

# Create a frame
frame1 = tk.Frame(root)
frame1.pack(side=tk.LEFT, padx=10, pady=10)

# Create widgets inside the frame
label1 = tk.Label(frame1, text="Subsection 1")
label1.pack()

button1 = tk.Button(frame1, text="Click me")
button1.pack()

# Create another frame
frame2 = tk.Frame(root)
frame2.pack(side=tk.RIGHT, padx=10, pady=10)

# Create widgets inside the second frame
label2 = tk.Label(frame2, text="Subsection 2")
label2.pack()

button2 = tk.Button(frame2, text="Press me")
button2.pack()

root.mainloop()