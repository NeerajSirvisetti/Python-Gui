import os
import subprocess
from threading import Thread
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QComboBox, QPushButton, QTextEdit, QLabel, QFileDialog

from file_checker import FileChecker  # Importing FileChecker class


class ApicGui(QMainWindow):

  def __init__(self, steps, folder_path):
    super(ApicGui, self).__init__()

    self.steps = steps
    self.folder_path_to_monitor = folder_path

    self.setWindowTitle(
        f"APIC FLOW: {subprocess.run(['pwd'], capture_output=True, text=True).stdout.strip()}"
    )
    self.setGeometry(100, 100, 800, 600)

    self.dbs_folder = "DBS"
    self.rpt_folder = "RPT"
    self.summary_folder = "Summary"
    self.backup_folder = "OLD_Backup"

    for folder in [
        self.dbs_folder, self.rpt_folder, self.summary_folder,
        self.backup_folder
    ]:
      os.makedirs(folder, exist_ok=True)

    self.init_ui()

    self.action_completed = {step: False for step in self.steps}

    self.file_checker = FileChecker(folder_path, steps, self.update_status)
    self.file_checker.start_monitoring()

  def init_ui(self):
    central_widget = QFrame(self)
    self.setCentralWidget(central_widget)

    layout = QVBoxLayout(central_widget)

    self.dropdown = QComboBox(self)
    self.dropdown.addItems(self.steps)
    layout.addWidget(self.dropdown)

    self.run_button = QPushButton("Run", self)
    self.run_button.clicked.connect(self.run_command)
    layout.addWidget(self.run_button)

    self.stop_button = QPushButton("Stop", self)
    self.stop_button.setDisabled(True)
    layout.addWidget(self.stop_button)

    self.refresh_button = QPushButton("Refresh", self)
    self.refresh_button.clicked.connect(self.inter)
    layout.addWidget(self.refresh_button)

    self.message_window_r2 = QTextEdit(self)
    self.message_window_r2.setReadOnly(True)
    layout.addWidget(self.message_window_r2)

    self.status_window_r3 = QTextEdit(self)
    self.status_window_r3.setReadOnly(True)
    layout.addWidget(self.status_window_r3)

    self.message_window_r4 = QTextEdit(self)
    self.message_window_r4.setReadOnly(True)
    layout.addWidget(self.message_window_r4)

    self.scrollbar_s2 = QTextEdit(self)
    self.scrollbar_s2.setReadOnly(True)
    layout.addWidget(self.scrollbar_s2)

    self.timer = QTimer(self)
    self.timer.timeout.connect(lambda: self.clear_message(self.scrollbar_s2))

    self.show()

  def update_status(self, step):
    self.steps.index(step)
    self.action_completed[step] = True
    self.update_completed_steps()

  def update_completed_steps(self):
    self.completed_steps = [
        step for step, completed in self.action_completed.items() if completed
    ]
    self.completed_index = sorted(
        [self.steps.index(i) for i in self.completed_steps])

    self.display_message(f"Status: {self.steps[self.completed_index[-1]]}",
                         self.status_window_r3,
                         disappear=False,
                         clear=True)

  def run_command(self):
    selected_step = self.dropdown.currentText()
    if self.action_completed[selected_step]:
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

  def execute_command_for_step(self, step):
    command = f"echo 'make {step}'"
    Thread(target=lambda: subprocess.run(command, shell=True)).start()

  def display_message(self,
                      message,
                      target_window,
                      disappear=True,
                      clear=True):
    target_window.setPlainText(message + "\n")
    if disappear:
      self.timer.start(3000)
    if clear:
      target_window.clear()

  def clear_message(self, target_window):
    target_window.clear()
    self.timer.stop()

  def ask_question(self, message):
    selected_step = self.dropdown.currentText()
    response = QMessageBox.question(self, selected_step, message,
                                    QMessageBox.Yes | QMessageBox.No)
    if response == QMessageBox.Yes:
      if QMessageBox.question(
          self, "Backup Confirmation",
          f"Do you want to backup files for steps after '{selected_step}'?",
          QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
        self.backup_files_after_selected_step(selected_step)
      message = f"Restarting '{selected_step}' command."
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

  def backup_files_after_selected_step(self, selected_step):
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
      file_link = QLabel(f"<a href=\"{report_file}\">{report_file}</a>", self)
      file_link.setOpenExternalLinks(True)
      self.message_window_r2.appendHtml(file_link.text())

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

  def stop_command(self):
    pass  # Add logic to stop the command (not provided in the original code)

  def inter(self):
    self.display_message("Restarting the application.",
                         self.message_window_s2,
                         disappear=False,
                         clear=True)
    QTimer.singleShot(1000, self.restart_application)

  def restart_application(self):
    python = sys.executable
    os.execl(python, python, *sys.argv)


if __name__ == "__main__":
  app = QApplication([])
  # List of steps
  steps = [
      "Synthesis", "Init", "Floorplan", "Powerplan", "Place", "PreCts", "Cts",
      "PostCts", "Route", "PostRoute", "Sign-off", "QRC", "STA", "Voltus"
  ]

  # Set the folder path to monitor
  folder_path_to_monitor = "./make/"

  # Calling the class
  gui = ApicGui(steps, folder_path_to_monitor)
  app.exec_()
