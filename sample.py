import tkinter as tk
from tkinter import ttk
import os
import subprocess
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


class ff_gui:

  def __init__(self, master, steps, folder_path):
    self.master = master
    self.update_window_size()

    self.steps = steps
    self.current_step = tk.StringVar()

    # Create a custom style for the Combobox
    self.style = ttk.Style()
    self.style.configure('custom.TCombobox',fieldbackground='white')

    # Dropdown to select steps
    self.step_dropdown = ttk.Combobox(master,
                                      textvariable=self.current_step,
                                      values=self.steps,
                                      state="readonly",
                                      style='custom.TCombobox')
    self.step_dropdown.bind("<<ComboboxSelected>>", self.update_step_buttons)
    self.step_dropdown.pack(side="left",padx=10, pady=10)
    #self.step_dropdown.pack(pady=10)

    # Buttons for selected step
    self.run_button = tk.Button(master,
                                text="Run",
                                command=self.run_command,
                                state=tk.DISABLED)
    self.run_button.pack(side="left", padx=10)
    self.stop_button = tk.Button(master,
                                 text="Stop",
                                 command=self.stop_command,
                                 state=tk.DISABLED)
    self.stop_button.pack(side="left", padx=5)

    # Message panels
    self.message_label = tk.Label(master,
                                  text="",
                                  bg="white",
                                  fg="black",
                                  font=("Helvetica", 10),
                                  anchor="w")
    self.message_label.pack(pady=10, padx=10, fill="both", expand=True)

    self.completed_steps_label = tk.Label(master,
                                          text="Completed Steps:",
                                          font=("Helvetica", 10),
                                          anchor="w")
    self.completed_steps_label.pack(pady=10, padx=10, fill="both", expand=True)

    # Initialize the file checker
    self.file_checker = FileChecker(folder_path, steps, self.update_box_color)
    self.file_checker.start_monitoring()

    # Track whether an action has already been completed
    self.action_completed = {step: False for step in self.steps}

    # Check for already completed steps at the start
    self.check_completed_steps_at_start()

    # Bind keys
    self.master.bind("<Control_L>e", self.on_key_exit)
    self.master.bind('<Control_L>r', self.on_key_restart)

  def update_window_size(self):
    screen_width = self.master.winfo_screenwidth()
    screen_height = self.master.winfo_screenheight()

    # Set the window size based on a percentage of the screen dimensions
    width_percentage = 0.8
    height_percentage = 0.8
    window_width = int(screen_width * width_percentage)
    window_height = int(screen_height * height_percentage)

    # Calculate the x and y positions to center the window
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    self.master.geometry(
        f"{window_width}x{window_height}+{x_position}+{y_position}")

  def check_completed_steps_at_start(self):
    for step in self.steps:
      file_path = os.path.join(folder_path_to_monitor, f"{step}")
      if os.path.exists(file_path):
        self.action_completed[step] = True

    # Update the completed steps label
    self.update_completed_steps()

  def update_step_buttons(self, event):
    selected_step = self.current_step.get()
    if selected_step:
      self.run_button.config(state=tk.NORMAL)
      self.stop_button.config(state=tk.DISABLED)

      if self.action_completed[selected_step]:
        # Check if the selected step is already completed
        self.display_message(f"Step '{selected_step}' is already completed.")
        self.style.configure("Custom.TCombobox", fieldbackground="green")
        #self.step_dropdown.configure(style='Yellow.TCombobox')
        self.run_button.config(state=tk.DISABLED)
    else:
      self.run_button.config(state=tk.DISABLED)
      self.stop_button.config(state=tk.DISABLED)

  def run_command(self):
    selected_step = self.current_step.get()
    if self.action_completed[selected_step]:
      # Check if the selected step is already completed
      self.display_message(f"Step '{selected_step}' is already completed.")
    else:
      self.display_message(f"Running '{selected_step}' command.")
      self.execute_command_for_step(selected_step)
      self.action_completed[selected_step] = True
      self.update_box_color(selected_step)
      self.update_completed_steps()

  def stop_command(self):
    selected_step = self.current_step.get()
    self.display_message(f"Stopping '{selected_step}' command.")
    # Add logic to stop the command (not provided in the original code)

  def execute_command_for_step(self, step):
    # Replace this function with the actual command you want to execute for each step
    command = f"echo 'make {step}'"
    Thread(target=lambda: subprocess.run(command, shell=True)).start()

  def update_completed_steps(self):
    self.completed_steps = [
        step for step, completed in self.action_completed.items() if completed
    ]
    self.completed_steps_label.config(
        text=f"Completed Steps: {', '.join(self.completed_steps)}")

  def display_message(self, message):
    self.message_label.config(text=message)
    self.master.after(3000, lambda: self.message_label.config(text="")
                      )  # Display message for 3 seconds

  def on_key_exit(self, event):
    self.display_message("Exiting the application.")
    self.file_checker.stop_monitoring()
    self.master.destroy()

  def update_box_color(self, step):
    index = self.steps.index(step)

  def on_key_restart(self, event):
    self.display_message("Restarting the application.")
    self.restart_application()

  def restart_application(self):
    python = sys.executable
    os.execl(python, python, *sys.argv)





Title = "APIC Flow:"+os.getcwd()
# Create the main window
root = tk.Tk()
root.title(f"{Title}")

# List of steps
steps = [
    "Init", "Floorplan", "Powerplan", "Place", "PreCts", "Cts", "PostCts",
    "Route", "PostRoute"
]

# Set the folder path to monitor
folder_path_to_monitor = "./make/"

# Calling the class
gui = ff_gui(root, steps, folder_path_to_monitor)

# Run the main loop
root.mainloop()
