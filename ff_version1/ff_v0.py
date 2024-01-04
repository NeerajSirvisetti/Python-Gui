import tkinter as tk
from tkinter import ttk

# Create the app class
class ff_gui:
  def __init__(self, master, steps):
    self.master = master
    # Set the master (the root window) to width and height
    master.geometry("600x800")
    # Create a label using ttk, give it master and text
    self.label = ttk.Label(master, text="Hello, Welcome to Foundation Flow Gui Wizard!")
    # Place it in the window a row, column
    #self.label.grid(row=0, column=0)
    
    self.steps = steps
    # Create a list to store box widgets
    self.boxes = []

    # Create boxes for each step
    for i in range(len(self.steps)):
        self.create_box(i)

    #Bind keys
    self.master.bind("<Control_L> e", exit)
    self.master.bind('<Control_L> i', self.on_key_Init)

  def on_key_Init(self, event):
    self.label.config(text="Key 'Return' pressed. Performing default action.")
    
  def on_box_select(self,index):
    # Change the color of the selected box
    self.boxes[index].config(bg="yellow")
    self.func = "on_key_{}".format(self.steps[index])
    self.func()

    # Execute the function linked to the selected box
    self.execute_function(index)

  def execute_function(self,index):
    # Replace this function with the actual function you want to execute
    print(f"Function for box {index + 1} executed.")

  # Function to create a box with a given index
  def create_box(self,index):
      self.box = tk.Button(self.master, text=self.steps[index], width=20, height=2, command=lambda i=index: self.on_box_select(i))
      self.box.pack(pady=5)
      self.boxes.append(self.box)





# Create the main window
root = tk.Tk()
root.title("Step Selector")

# List of steps
steps = ["Init", "Floorplan", "Powerplan", "Place", "PreCts", "Cts", "PostCts", "Route", "PostRoute"]


#calling the class
gui=ff_gui(root,steps)
# Run the main loop
root.mainloop()
