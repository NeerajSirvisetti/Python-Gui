import tkinter as tk
from tkinter import ttk
import os
import time
from threading import Thread

class FileChecker:
    def __init__(self, folder_path, target_files, callback):
        self.folder_path = folder_path
        self.target_files = target_files
        self.callback = callback
        self.is_running = False

    def start_monitoring(self):
        self.is_running = True
        Thread(target=self._monitor_folder).start()

    def stop_monitoring(self):
        self.is_running = False

    def _monitor_folder(self):
        while self.is_running:
            for target_file in self.target_files:
                file_path = os.path.join(self.folder_path, target_file)
                if os.path.exists(file_path):
                    self.callback(target_file)
            time.sleep(1)

class ff_gui:
    def __init__(self, master, steps, folder_path):
        self.master = master
        master.geometry("600x800")

        self.label = ttk.Label(master, text="Hello, Welcome to Foundation Flow Gui Wizard!")
        self.label.pack(pady=10)

        self.steps = steps
        self.boxes = []

        for i in range(len(self.steps)):
            self.create_box(i)

        # Bind keys
        self.master.bind("<Control_L>e", self.on_key_exit)
        self.master.bind('<Control_L>i', self.on_key_Init)

        # Initialize the file checker
        self.file_checker = FileChecker(folder_path, steps, self.update_box_color)
        self.file_checker.start_monitoring()

        # Track whether an action has already been completed
        self.action_completed = [False] * len(self.steps)

    def on_key_Init(self, event):
        if not self.action_completed[0]:
            self.label.config(text="Key 'Ctrl+I' pressed. Performing 'Init' action.")
            # Simulate some action for 'Init'
            self.action_completed[0] = True
            self.update_box_color("Init")
        else:
            self.label.config(text="Action already completed for 'Init'.")

    def on_key_exit(self, event):
        self.label.config(text="Key 'Ctrl+E' pressed. Exiting the application.")
        self.file_checker.stop_monitoring()
        self.master.destroy()

    def on_box_select(self, index):
        if self.action_completed[index]:
            self.label.config(text=f"Action already completed for '{self.steps[index]}'.")
        else:
            self.boxes[index].config(bg="yellow")
            self.execute_function(index)

    def execute_function(self, index):
        # Replace this function with the actual function you want to execute
        print(f"Function for box {index + 1} executed.")
        self.action_completed[index] = True
        self.update_box_color(self.steps[index])

    def update_box_color(self, step):
        index = self.steps.index(step)
        self.boxes[index].config(bg="green")

    def create_box(self, index):
        box = tk.Button(self.master, text=self.steps[index], width=20, height=2, command=lambda i=index: self.on_box_select(i))
        box.pack(pady=5)
        self.boxes.append(box)

# Create the main window
root = tk.Tk()
root.title("Step Selector")

# List of steps
steps = ["Init", "Floorplan", "Powerplan", "Place", "PreCts", "Cts", "PostCts", "Route", "PostRoute"]

# Set the folder path to monitor
folder_path_to_monitor = "./make/"

# Calling the class
gui = ff_gui(root, steps, folder_path_to_monitor)

# Run the main loop
root.mainloop()
