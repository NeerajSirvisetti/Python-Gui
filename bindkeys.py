import tkinter as tk

class GUIWithKeyBindings:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.label = tk.Label(self.root, text="Press keys 'A' or 'B'")
        self.label.pack(pady=10)

        # Bind the 'A' key to the on_key_a function
        self.root.bind('a', self.on_key_a)

        # Bind the 'B' key to the on_key_b function
        self.root.bind('b', self.on_key_b)

        # Bind the 'Escape' key to the on_key_escape function
        self.root.bind('<Escape>', self.on_key_escape)

        # Bind the 'Return' key to the on_key_return function
        self.root.bind('<Control_L> r', self.on_key_return)

    def on_key_escape(self, event):
        self.label.config(text="Key 'Escape' pressed. Exiting the application.")
        self.root.destroy()

    def on_key_return(self, event):
        self.label.config(text="Key 'Return' pressed. Performing default action.")
        self.perform_default_action()

    def perform_default_action(self):
        # Replace this with the action you want for the default key
        print("Default action executed.")

    def on_key_a(self, event):
        self.label.config(text="Key 'A' pressed. Executing Function A.")
        self.execute_function_a()

    def on_key_b(self, event):
        self.label.config(text="Key 'B' pressed. Executing Function B.")
        self.execute_function_b()

    def execute_function_a(self):
        # Replace this with the action you want for key 'A'
        print("Function A executed.")

    def execute_function_b(self):
        # Replace this with the action you want for key 'B'
        print("Function B executed.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Key Binding Example")

    gui = GUIWithKeyBindings(root)

    root.mainloop()
