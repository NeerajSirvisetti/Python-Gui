import tkinter as tk
from tkinter import ttk
from datetime import datetime
import subprocess
import os
from threading import Thread
import sys
import time


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


class ApicGui:
    def __init__(self, root, steps, folder_path ):
        self.steps = steps
        self.root = root
        self.folder_path_to_monitor = folder_path
        #self.root.geometry("800x600")
        self.update_window_size()

        self.root.title(f"APIC FLOW: {subprocess.run(['pwd'], capture_output=True, text=True).stdout.strip()}")
        #print(os.getcwd())
        # Section 1
        self.section1 = tk.Frame(root, bd=2, relief=tk.GROOVE)
        self.section1.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        # Subsections in Section 1
        r1_height = 1/8
        r2_height = 3/4
        r3_height = r4_height = 1/16

        self.r1 = tk.Frame(self.section1, bd=2, relief=tk.GROOVE)
        self.r1.place(relx=0, rely=0, relwidth=1, relheight=r1_height)

        self.r2 = tk.Frame(self.section1, bd=2, relief=tk.GROOVE)
        self.r2.place(relx=0, rely=r1_height, relwidth=1, relheight=r2_height)

        self.r3 = tk.Frame(self.section1, bd=2, relief=tk.GROOVE)
        self.r3.place(relx=0, rely=r1_height+r2_height, relwidth=1, relheight=r3_height)

        self.r4 = tk.Frame(self.section1, bd=2, relief=tk.GROOVE)
        self.r4.place(relx=0, rely=r1_height+r2_height+r3_height, relwidth=1, relheight=r4_height)

        # Widgets in r1
        self.options = self.steps
        self.selected_option = tk.StringVar()
        self.selected_option.set("Select the Stage")

        self.dropdown = ttk.Combobox(self.r1, values=self.options,state="readonly",textvariable=self.selected_option)
        self.dropdown.pack(side=tk.LEFT, padx=5)

        self.run_button = tk.Button(self.r1, text="Run", command=self.run_command)
        self.run_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.r1, text="Stop", state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.refresh_button = tk.Button(self.r1, text="Refresh", command=self.inter)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        # Widgets in r2
        self.scrollbar_r2 = tk.Scrollbar(self.r2)
        self.scrollbar_r2.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_window_r2 = tk.Text(self.r2, wrap="word", yscrollcommand=self.scrollbar_r2.set, state=tk.DISABLED)
        self.message_window_r2.pack(expand=True, fill=tk.BOTH)
        self.scrollbar_r2.config(command=self.message_window_r2.yview)  

        # Widgets in r3
        #self.status_window_r3 = tk.Label(self.r3, text=self.get_current_time_date())
        self.status_window_r3 = tk.Text(self.r3, wrap="word", state=tk.DISABLED)
        self.status_window_r3.pack(expand=True, fill=tk.BOTH)
        self.display_message("",self.status_window_r3,disappear=False, clear=True)


        # Widgets in r4
        self.message_window_r4 = tk.Text(self.r4, wrap="word", state=tk.DISABLED)
        self.message_window_r4.pack(expand=True, fill=tk.BOTH)

        # Section 2
        self.section2 = tk.Frame(root, bd=2, relief=tk.GROOVE)
        self.section2.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        self.scrollbar_s2 = tk.Scrollbar(self.section2)
        self.scrollbar_s2.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_window_s2 = tk.Text(self.section2, wrap="word", yscrollcommand=self.scrollbar_s2.set, state=tk.DISABLED)
        self.message_window_s2.pack(expand=True, fill=tk.BOTH)
        self.scrollbar_s2.config(command=self.message_window_s2.yview)  

        # Track whether an action has already been completed
        self.action_completed = {step: False for step in self.steps}


        # Initialize the file checker
        self.file_checker = FileChecker(folder_path, steps, self.update_status)
        self.file_checker.start_monitoring()

        # Check for already completed steps at the start
        self.check_completed_steps_at_start()

        # Bind keys
        self.root.bind("<Control_L>e", self.on_key_exit)
        self.root.bind('<Control_L>r', self.on_key_restart)

    def update_window_size(self):
      screen_width = self.root.winfo_screenwidth()
      screen_height = self.root.winfo_screenheight()

      # Set the window size based on a percentage of the screen dimensions
      width_percentage = 0.8
      height_percentage = 0.8
      window_width = int(screen_width * width_percentage)
      window_height = int(screen_height * height_percentage)

      # Calculate the x and y positions to center the window
      x_position = (screen_width - window_width) // 2
      y_position = (screen_height - window_height) // 2

      self.root.geometry(
          f"{window_width}x{window_height}+{x_position}+{y_position}")

    def check_completed_steps_at_start(self):
        for step in self.steps:
          file_path = os.path.join(folder_path_to_monitor, f"{step}")
          #print(file_path)
          if os.path.exists(file_path):
            self.action_completed[step] = True

        # Update the completed steps label
        self.update_completed_steps()

    def update_completed_steps(self):
        self.completed_steps = [step for step, completed in self.action_completed.items() if completed]
        self.completed_index = []
        for i in self.completed_steps:
          self.completed_index.append(self.steps.index(i))
        self.completed_index.sort()
        #print(f"completed indexs:{self.completed_index},completed steps:{self.completed_steps},steps:{self.steps}")
        #self.display_message(f"Completed Steps: {', '.join(self.completed_steps)}\nStatus: {self.steps[self.completed_index[-1]]}",self.status_window_r3, disappear=False, clear=True)
        self.display_message(f"Status: {self.steps[self.completed_index[-1]]}",self.status_window_r3, disappear=False, clear=True)


    def run_command(self):
        selected_step = self.selected_option.get()
        if self.action_completed[selected_step]:
          # Check if the selected step is already completed
          self.display_message(f"Step '{selected_step}' is already completed.",self.message_window_s2, disappear=True, clear=True)
        else:
          self.display_message(f"Running '{selected_step}' command.",self.message_window_s2, disappear=True, clear=True)
          self.execute_command_for_step(selected_step)
          self.action_completed[selected_step] = True
          self.update_status(selected_step)
          self.update_completed_steps()

    def stop_command(self):
        selected_step = self.selected_option.get()
        self.display_message(f"Stopping '{selected_step}' command.",self.message_window_s2, disappear=True, clear=True)
        # Add logic to stop the command (not provided in the original code)

    def execute_command_for_step(self, step):
        # Replace this function with the actual command you want to execute for each step
        command = f"echo 'make {step}'"
        Thread(target=lambda: subprocess.run(command, shell=True)).start()


    def get_current_time_date(self):
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def display_message(self, message, target_window, disappear=True, clear=True):
        target_window.config(state=tk.NORMAL)
        if clear:
            target_window.delete(1.0, tk.END)
        target_window.insert(tk.END, message + "\n")
        if disappear:
            self.root.after(3000, lambda: self.clear_message(target_window))
        target_window.config(state=tk.DISABLED)

    def clear_message(self, target_window):
        target_window.config(state=tk.NORMAL)
        target_window.delete(1.0, tk.END)
        target_window.config(state=tk.DISABLED)
      
    def update_status(self, step):
        index = self.steps.index(step)
        self.action_completed[step] = True
        self.update_completed_steps()


    def on_key_exit(self, event):
        self.display_message("Exiting the application.", self.message_window_s2, disappear=False, clear=True)
        self.root.after(1000, self.root.destroy)
      

    def on_key_restart(self, event):
        self.inter()

    def inter(self):
        self.display_message("Restarting the application.", self.message_window_s2, disappear=False, clear=True)
        self.root.after(1000, self.restart_application)
      
    def restart_application(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)


if __name__ == "__main__":
    root = tk.Tk()
 
    # List of steps
    steps = [
        "Synthesis","Init", "Floorplan", "Powerplan", "Place", "PreCts", "Cts", "PostCts",
        "Route", "PostRoute","Sign-off","QRC","STA","Voltus"
    ]

    # Set the folder path to monitor
    folder_path_to_monitor = "./make/"

    # Calling the class
    gui = ApicGui(root, steps, folder_path_to_monitor)
    root.mainloop()