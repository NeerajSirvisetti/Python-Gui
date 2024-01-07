
# **Version3**

## **Version3.1**
### `FileChecker` Class
- Monitors a specified folder for the existence of target files.
- It runs in a separate thread (`_monitor_folder` method) and periodically checks if the target files exist in the specified folder.
- Calls a user-provided callback (`callback`) when a target file is found.

### `ApicGui` Class
- Represents the main GUI application.
- Divides the main window into two sections: Section 1 and Section 2.

#### Section 1
- Contains multiple frames (`r1`, `r2`, `r3`, `r4`) for organizing widgets.
- Uses a custom style for the Tkinter Combobox (`dropdown`).
- Provides a Combobox for selecting a step, along with buttons for running, stopping, and refreshing.
- Displays messages and statuses in separate text widgets (`message_window_r2`, `status_window_r3`, `message_window_r4`).
- Initializes a `FileChecker` instance to monitor a specified folder for steps and updates the GUI when steps are completed.

#### Section 2
- Displays messages and logs related to the application's progress in a separate text widget (`message_window_s2`).

#### Functionality
- Tracks the completion status of each step using the `action_completed` dictionary.
- Allows users to run a step and displays corresponding messages.
- Checks if a step is already completed and prompts the user to restart if necessary.
- Updates the status of completed steps and provides an option to restart from a specific step, marking subsequent steps as incomplete.

#### Keyboard Shortcuts
- The application responds to keyboard shortcuts:
  - `Ctrl + e`: Exits the application.
  - `Ctrl + r`: Restarts the application.

### Usage
- The script defines a list of steps and a folder path to monitor (`steps` and `folder_path_to_monitor`).
- Creates an instance of the `ApicGui` class, passing the list of steps and folder path.
- Starts the Tkinter main loop (`root.mainloop()`).

### Note
- The actual command executed for each step (e.g., `echo 'make {step}'`) is a placeholder and should be replaced with the desired functionality.

Overall, this script provides a foundation for a GUI-based application to monitor and manage a multi-step process. Users can interact with the GUI to run and monitor different steps in the process.

## **Version3.2**
