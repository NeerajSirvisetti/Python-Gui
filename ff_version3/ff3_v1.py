import tkinter as tk
from tkinter import ttk
from datetime import datetime
import subprocess
import os
import sys


class ApicGui:
    def __init__(self, root, steps, folder_path_to_monitor ):
        self.steps = steps
        self.root = root
        self.root.geometry("800x600")
        self.root.title(f"APIC FLOW: {subprocess.run(['pwd'], capture_output=True, text=True).stdout.strip()}")

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

        self.dropdown = ttk.Combobox(self.r1, values=self.options, textvariable=self.selected_option)
        self.dropdown.pack(side=tk.LEFT, padx=5)

        self.run_button = tk.Button(self.r1, text="Run", command=self.run_command)
        self.run_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.r1, text="Stop", state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.refresh_button = tk.Button(self.r1, text="Refresh", command=self.restart_application)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        # Widgets in r2
        self.scrollbar_r2 = tk.Scrollbar(self.r2)
        self.scrollbar_r2.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_window_r2 = tk.Text(self.r2, wrap="word", yscrollcommand=self.scrollbar_r2.set, state=tk.DISABLED)
        self.message_window_r2.pack(expand=True, fill=tk.BOTH)

        # Widgets in r3
        self.status_window_r3 = tk.Label(self.r3, text=self.get_current_time_date())
        self.status_window_r3.pack(expand=True, fill=tk.BOTH)

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

        # Bind keys
        self.root.bind("<Control_L>e", self.on_key_exit)
        self.root.bind('<Control_L>r', self.on_key_restart)

    def run_command(self):
        selected_option = self.selected_option.get()
        # Add logic to run command based on the selected_option
        # Update message window_r2 with the command execution result

    def refresh_gui(self):
        # Add logic to refresh the GUI, e.g., restart the application
        pass

    def get_current_time_date(self):
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def display_message(self, message, target_window):
        target_window.config(state=tk.NORMAL)
        target_window.insert(tk.END, message + "\n")
        target_window.config(state=tk.DISABLED)
        self.root.after(3000, lambda: target_window.delete(1.0, tk.END))  # Display message for 3 seconds

    def on_key_exit(self, event):
        self.display_message("Exiting the application.", self.message_window_s2)
        self.root.destroy()

    def on_key_restart(self, event):
        self.display_message("Restarting the application.", self.message_window_s2)
        self.restart_application()

    def restart_application(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)


if __name__ == "__main__":
    root = tk.Tk()
 
    # List of steps
    steps = [
        "Init", "Floorplan", "Powerplan", "Place", "PreCts", "Cts", "PostCts",
        "Route", "PostRoute"
    ]

    # Set the folder path to monitor
    folder_path_to_monitor = "./make/"

    # Calling the class
    gui = ApicGui(root, steps, folder_path_to_monitor)
    root.mainloop()