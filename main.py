import tkinter as tk
from tkinter import ttk
import time

# Create the app class
class App:
  def __init__(self, master):
    self.master = master
    # Set the master (the root window) to width and height
    master.geometry("600x400")
    # Create a label using ttk, give it master and text
    self.label = ttk.Label(master, text="Hello, Welcome to Foundation Flow Gui Wizard!")
    # Place it in the window a row, column
    self.label.grid(row=0, column=0)
    self.show(master,"Init",1)
    self.show(master,"Floorplan",2)
    master.bind("<Control_L> e", exit)
  def show(self,master,text,i):

    # Create a label using ttk, give it master and text and set the command callback to Init
    self.button = ttk.Button(master, text=text, command=self.Init)
    # Place it in the window a row, column
    self.button.grid(row=i, column=1)
    
    
  def Init(self):
    # If button is pressed, then set press text to Hello there user! 
    self.press.config(text="Initializing Completed")
    # Create a label, give it master but no text
    self.press = ttk.Label(self.master)
    # Place it in the window a row, column
    self.press.grid(row=1, column=0)

   


# Make the master (root window)
root = tk.Tk()
# Make the app and pass it the master (root window)
app = App(root)
# Run the master (root window)
root.mainloop()