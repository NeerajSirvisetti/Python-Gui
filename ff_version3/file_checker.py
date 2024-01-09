# file_checker.py

import os
from threading import Thread
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
      if self.is_running:
        time.sleep(1000)
