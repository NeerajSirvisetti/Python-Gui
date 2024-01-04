import tkinter as tk

root = tk.Tk()

label1 = tk.Label(root, text="Left Aligned")
label1.pack(side=tk.LEFT)

label2 = tk.Label(root, text="Center Aligned")
label2.pack()

label3 = tk.Label(root, text="Right Aligned")
label3.pack(side=tk.RIGHT)

root.mainloop()