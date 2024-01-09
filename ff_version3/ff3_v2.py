import os
import subprocess
import sys
import tkinter as tk
from threading import Thread
from tkinter import messagebox, ttk
import shutil
from file_checker import FileChecker  # Importing FileChecker class
import webbrowser


class ApicGui:

  def __init__(self, root, steps, folder_path):
    self.steps = steps
    self.root = root
    self.folder_path_to_monitor = folder_path
    #self.root.geometry("800x600")
    self.update_window_size()

    self.root.title(
        f"APIC FLOW: {subprocess.run(['pwd'], capture_output=True, text=True).stdout.strip()}"
    )

    # Additional folders to track
    self.dbs_folder = "DBS"
    self.rpt_folder = "RPT"
    self.summary_folder = "Summary"
    self.backup_folder = "OLD_Backup"

    # Create folders if they don't exist
    for folder in [
        self.dbs_folder, self.rpt_folder, self.summary_folder,
        self.backup_folder
    ]:
      os.makedirs(folder, exist_ok=True)

    # Section 1
    self.section1 = tk.Frame(root, bd=2, relief=tk.GROOVE)
    self.section1.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    # Subsections in Section 1
    r1_height = 1 / 8
    r2_height = 3 / 4
    r3_height = r4_height = 1 / 16

    self.r1 = tk.Frame(self.section1, bd=2, relief=tk.GROOVE)
    self.r1.place(relx=0, rely=0, relwidth=1, relheight=r1_height)

    self.r2 = tk.Frame(self.section1, bd=2, relief=tk.GROOVE)
    self.r2.place(relx=0, rely=r1_height, relwidth=1, relheight=r2_height)

    self.r3 = tk.Frame(self.section1, bd=2, relief=tk.GROOVE)
    self.r3.place(relx=0,
                  rely=r1_height + r2_height,
                  relwidth=1,
                  relheight=r3_height)

    self.r4 = tk.Frame(self.section1, bd=2, relief=tk.GROOVE)
    self.r4.place(relx=0,
                  rely=r1_height + r2_height + r3_height,
                  relwidth=1,
                  relheight=r4_height)

    # Configure the custom style before creating the combobox
    self.style = ttk.Style()
    self.style.configure("Custom.TCombobox", fieldbackground="white")

    # Widgets in r1
    self.options = self.steps
    self.selected_option = tk.StringVar()
    self.selected_option.set("Select the Stage")

    self.dropdown = ttk.Combobox(self.r1,
                                 values=self.options,
                                 state="readonly",
                                 textvariable=self.selected_option)
    self.dropdown.pack(side=tk.LEFT, padx=5)
    self.dropdown.configure(style="Custom.TCombobox")

    self.run_button = tk.Button(self.r1, text="Run", command=self.run_command)
    self.run_button.pack(side=tk.LEFT, padx=5)

    self.stop_button = tk.Button(self.r1, text="Stop", state=tk.DISABLED)
    self.stop_button.pack(side=tk.LEFT, padx=5)

    self.refresh_button = tk.Button(self.r1,
                                    text="Refresh",
                                    command=self.inter)
    self.refresh_button.pack(side=tk.LEFT, padx=5)

    # Widgets in r2
    self.scrollbar_r2 = tk.Scrollbar(self.r2)
    self.scrollbar_r2.pack(side=tk.RIGHT, fill=tk.Y)

    self.message_window_r2 = tk.Text(self.r2,
                                     wrap="word",
                                     yscrollcommand=self.scrollbar_r2.set,
                                     state=tk.DISABLED)
    self.message_window_r2.pack(expand=True, fill=tk.BOTH)
    self.scrollbar_r2.config(command=self.message_window_r2.yview)

    # Widgets in r3
    self.status_window_r3 = tk.Text(self.r3, wrap="word", state=tk.DISABLED)
    self.status_window_r3.pack(expand=True, fill=tk.BOTH)
    self.display_message("",
                         self.status_window_r3,
                         disappear=False,
                         clear=True)

    # Widgets in r4
    self.message_window_r4 = tk.Text(self.r4, wrap="word", state=tk.DISABLED)
    self.message_window_r4.pack(expand=True, fill=tk.BOTH)

    # Section 2
    self.section2 = tk.Frame(root, bd=2, relief=tk.GROOVE)
    self.section2.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    self.scrollbar_s2 = tk.Scrollbar(self.section2)
    self.scrollbar_s2.pack(side=tk.RIGHT, fill=tk.Y)

    self.message_window_s2 = tk.Text(self.section2,
                                     wrap="word",
                                     yscrollcommand=self.scrollbar_s2.set,
                                     state=tk.DISABLED)
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
    self.dropdown.bind("<FocusIn>", self.on_combobox_focus)
    self.dropdown.bind("<FocusOut>", self.on_combobox_focus)

  def on_combobox_focus(self, event):
    selected_step = self.selected_option.get()
    if (selected_step
        in self.steps) and (self.action_completed[selected_step]):
      self.style.configure("Custom.TCombobox", fieldbackground="green")
      self.show_report_files(selected_step)
      self.show_summary_content(selected_step)
    else:
      self.style.configure("Custom.TCombobox", fieldbackground="white")
      self.display_message(f"{selected_step} is yet to be Completed",
                           self.message_window_r2,
                           disappear=False,
                           clear=True)
      self.display_message(f"{selected_step} is yet to be Completed",
                           self.message_window_s2,
                           disappear=False,
                           clear=True)

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
    self.completed_steps = [
        step for step, completed in self.action_completed.items() if completed
    ]
    self.completed_index = []
    for i in self.completed_steps:
      self.completed_index.append(self.steps.index(i))
    self.completed_index.sort()

    self.display_message(f"Status: {self.steps[self.completed_index[-1]]}",
                         self.status_window_r3,
                         disappear=False,
                         clear=True)

  def run_command(self):
    selected_step = self.selected_option.get()
    if self.action_completed[selected_step]:
      # Check if the selected step is already completed
      self.ask_question(
          f"Step '{selected_step}' is already completed.\nDo you want to Restart?"
      )

    else:
      self.display_message(f"Running '{selected_step}' command.",
                           self.message_window_s2,
                           disappear=True,
                           clear=True)
      self.execute_command_for_step(selected_step)
      self.action_completed[selected_step] = True
      self.update_status(selected_step)
      self.update_completed_steps()
      self.show_report_files(selected_step)
      self.show_summary_content(selected_step)

  def stop_command(self):
    selected_step = self.selected_option.get()
    self.display_message(f"Stopping '{selected_step}' command.",
                         self.message_window_s2,
                         disappear=True,
                         clear=True)
    # Add logic to stop the command (not provided in the original code)

  def execute_command_for_step(self, step):
    # Replace this function with the actual command you want to execute for each step
    command = f"echo 'make {step}'"
    Thread(target=lambda: subprocess.run(command, shell=True)).start()

  def display_message(self,
                      message,
                      target_window,
                      disappear=True,
                      clear=True):
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
    self.steps.index(step)
    self.action_completed[step] = True
    self.update_completed_steps()

  def backup_files_after_selected_step(self, selected_step):
    # Backup files from RPT, DBS, make, Summary folders to OLD_Backup folder
    for step in self.steps[self.steps.index(selected_step) + 1:]:
      self.backup_folder_contents(step, self.rpt_folder)
      self.backup_folder_contents(step, self.dbs_folder)
      self.backup_folder_contents(step, self.folder_path_to_monitor)
      self.backup_folder_contents(step, self.summary_folder)

  def backup_folder_contents(self, step, source_folder):
    source_pattern = f"{step}*"
    source_files = [
        f for f in os.listdir(source_folder) if f.startswith(source_pattern)
    ]
    for source_file in source_files:
      source_file_path = os.path.join(source_folder, source_file)
      destination_file_path = os.path.join(self.backup_folder, source_file)
      shutil.move(source_file_path, destination_file_path)
    # Note: This will replace existing files with the same name in the backup folder

  def show_report_files(self, selected_step):
    report_files = self.get_report_files(selected_step)
    if report_files:
      self.display_report_files(report_files)
    else:
      self.display_message(
          f"Report Files have not been generated for this {selected_step}.",
          self.message_window_r2,
          disappear=False,
          clear=True)

  def get_report_files(self, selected_step):
    report_files_pattern = f"{selected_step}"
    return [
        f for f in os.listdir(self.rpt_folder)
        if f.startswith(report_files_pattern)
    ]

  def display_report_files(self, report_files):
    self.display_message("Report Files:",
                         self.message_window_r2,
                         disappear=False,
                         clear=True)
    for report_file in report_files:
      file_link = tk.Label(self.r2,
                           text=report_file,
                           fg="blue",
                           cursor="hand2")
      file_link.pack()
      file_link.bind(
          "<Button-1>",
          lambda event, file=report_file: self.open_file_contents(file))

  def open_file_contents(self, file_name):
    file_path = os.path.join(self.rpt_folder, file_name)
    with open(file_path, 'r') as file:
      contents = file.read()
      self.display_message(contents,
                           self.message_window_s2,
                           disappear=False,
                           clear=True)

  def show_summary_content(self, selected_step):
    summary_file = self.get_summary_file(selected_step)
    if summary_file:
      self.display_summary_content(summary_file)
    else:
      self.display_message(
          f"Summary File has not been generated for this {selected_step}.",
          self.message_window_s2,
          disappear=False,
          clear=True)

  def get_summary_file(self, selected_step):
    summary_file = f"{selected_step}"
    matching_files = [
        f for f in os.listdir(self.summary_folder)
        if f.startswith(summary_file)
    ]
    return matching_files[0] if matching_files else None

  def display_summary_content(self, summary_file):
    summary_file_path = os.path.join(self.summary_folder, summary_file)
    with open(summary_file_path, 'r') as file:
      contents = file.read()
      self.display_message(contents,
                           self.message_window_s2,
                           disappear=False,
                           clear=True)

  def ask_question(self, message):
    selected_step = self.selected_option.get()
    response = messagebox.askyesno(selected_step, message)
    if response:
      # After running, move files to backup if needed
      if messagebox.askyesno(
          "Backup Confirmation",
          f"Do you want to backup files for steps after '{selected_step}'?"):
        self.backup_files_after_selected_step(selected_step)
      message = f"Restarting '{selected_step}' command."
      # Mark steps after the selected step as completed
      selected_index = self.steps.index(selected_step)
      for step in self.steps[selected_index + 1:]:
        self.action_completed[step] = False
      self.update_completed_steps()
    else:
      message = f"Stopping the restart of '{selected_step}' command."
    self.display_message(message,
                         self.message_window_s2,
                         disappear=True,
                         clear=True)
    self.show_report_files(selected_step)
    self.show_summary_content(selected_step)

  def on_key_exit(self, event):
    self.display_message("Exiting the application.",
                         self.message_window_s2,
                         disappear=False,
                         clear=True)
    self.root.after(1000, self.root.destroy)

  def on_key_restart(self, event):
    self.inter()

  def inter(self):
    self.display_message("Restarting the application.",
                         self.message_window_s2,
                         disappear=False,
                         clear=True)
    self.root.after(1000, self.restart_application)

  def restart_application(self):
    python = sys.executable
    os.execl(python, python, *sys.argv)


if __name__ == "__main__":
  root = tk.Tk()

  # List of steps
  steps = [
      "Synthesis", "Init", "Floorplan", "Powerplan", "Place", "PreCts", "Cts",
      "PostCts", "Route", "PostRoute", "Sign-off", "QRC", "STA", "Voltus"
  ]

  # Set the folder path to monitor
  folder_path_to_monitor = "./make/"

  # Calling the class
  gui = ApicGui(root, steps, folder_path_to_monitor)
  root.mainloop()
