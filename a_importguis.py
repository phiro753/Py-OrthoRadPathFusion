"""
Description: Script for creating different GUI that can be employed/used in b_Main file

History:
> Initially created by Robert Phillips 2024-06
> Docstring notes by Jaime Uy De Baron 2025-06
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os

class StringReturn: 
    """ A class that creates an entire GUI for end-users to input information about the specimen """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('User Input')

        # Create a label
        self.label = tk.Label(self.root, text="A short filename suffix for which bisection this is/method used (e.g. M3_Med or M1_L for Medial or Lateral)")
        self.label.pack()

        # Create an entry widget
        self.entry = tk.Entry(self.root)
        self.entry.pack()
        self.entry.focus_set()
        self.user_input = None  # Will hold user input

        # Create the okay button
        self.ok_button = tk.Button(self.root, text='Okay', command=self.get_input_and_close) 
        self.ok_button.pack(side='bottom')

        # Bind the Enter key to the same function
        self.root.bind('<Return>', lambda event: self.get_input_and_close())

    def get_input_and_close(self):
        """ Store user input and close the window """
        self.user_input = self.entry.get()
        self.root.quit()  # Quit the main loop
        self.root.destroy()  # Destroy the window to clean up

    def run(self):
        """ Start the GUI main loop """
        self.root.mainloop()
        return self.user_input


class FileSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main tkinter window

    def select_file(self):
        initial_dir = os.getcwd()  # Start from the current working directory
        file_path = filedialog.askopenfilename(initialdir=initial_dir)
        return file_path

class MethodSelector:
    def __init__(self):
        self.selected_method = None  # Store the selected method

    def run(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Select Method")
        self.root.geometry("300x200")  # Set a reasonable size

        # Add instructions
        label = tk.Label(self.root, text="Please select a method:", font=("Arial", 12))
        label.pack(pady=10)

        # Add buttons for M1, M2, and M3
        button_m1 = tk.Button(self.root, text="Method 1 (M1)", command=lambda: self.select_method(1))
        button_m1.pack(pady=5)

        button_m2 = tk.Button(self.root, text="Method 2 (M2)", command=lambda: self.select_method(2))
        button_m2.pack(pady=5)

        button_m3 = tk.Button(self.root, text="Method 3 (M3)", command=lambda: self.select_method(3))
        button_m3.pack(pady=5)

        # Start the GUI loop
        self.root.mainloop()

        # Return the selected method as an integer
        return self.get_selected_method()

    def select_method(self, method_number):
        # Set the selected method
        self.selected_method = method_number
        # Show a confirmation message
        messagebox.showinfo("Method Selected", f"You selected Method {method_number}.")
        # Close the GUI window
        self.root.destroy()

    def get_selected_method(self):
        """Returns 1 for M1, 2 for M2, 3 for M3, or None if no selection was made."""
        return self.selected_method

class OutputDecision:
    def __init__(self):
        self.output_directory = None

    def run(self):
        root = tk.Tk()
        root.title("Save Planes?")

        message = tk.Label(root, text="Do you want to save planes to a folder?")
        message.pack()

        def handle_yes():
            self.output_directory = filedialog.askdirectory(initialdir=os.getcwd())
            root.quit()  # Exit the event loop
            root.destroy()  # Close the window

        def handle_no():
            root.quit()  # Exit the event loop
            root.destroy()  # Close the window

        yes_button = tk.Button(root, text="Yes", command=handle_yes)
        yes_button.pack(side="left", padx=10)

        no_button = tk.Button(root, text="No", command=handle_no)
        no_button.pack(side="right", padx=10)

        root.mainloop()  # Start the GUI loop
        return self.output_directory


class NumberTableGUI:
    ''' Table of laboratory vernier caliper measurements. '''
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Number Table")
        self.table = []

        # Create widgets
        self.label = tk.Label(
            self.root, 
            text="Enter two numbers separated by spaces (e.g., '12.5 14.8'):"
        )
        self.entry = tk.Entry(self.root)
        self.add_button = tk.Button(self.root, text="Add Row", command=self.add_row)
        self.subtract_button = tk.Button(self.root, text="Remove Last Row", command=self.subtract_row)
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_matrix)
        self.matrix_label = tk.Label(self.root, text="Measurements (columns: da, db):")

        # Grid layout
        self.label.grid(row=0, column=0, columnspan=2, pady=5)
        self.entry.grid(row=1, column=0, columnspan=2, pady=5)
        self.add_button.grid(row=2, column=0, pady=5)
        self.subtract_button.grid(row=2, column=1, pady=5)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=5)
        self.matrix_label.grid(row=4, column=0, columnspan=2, pady=5)

    def add_row(self):
        """ Add a new row to the table based on user input """
        row_values = self.entry.get().strip().split()  # Split input by spaces
        if len(row_values) == 2:  # Ensure exactly 2 values are entered
            try:
                self.table.append([float(val) for val in row_values])
                self.update_matrix_label()
                self.entry.delete(0, tk.END)  # Clear input field
            except ValueError:
                print("Invalid input. Please enter numeric values.")
        else:
            print("Please enter exactly 2 values for each row.")

    def subtract_row(self):
        """ Remove the last row from the table """
        if self.table:
            self.table.pop()
            self.update_matrix_label()
        else:
            print("No rows to remove.")

    def submit_matrix(self):
        """ Submit the matrix and close the window """
        print("Submitted Matrix:", self.table)
        self.root.quit()  # Exit the main loop
        self.root.destroy()  # Close the window

    def update_matrix_label(self):
        """ Update the display of the matrix of measurements """
        # Format rows for display
        matrix_text = "\n".join([f"{row[0]:.2f}  {row[1]:.2f}" for row in self.table])
        self.matrix_label.config(text=f"Measurements (columns: da, db):\n{matrix_text}")

    def run(self):
        """ Start the GUI main loop """
        self.root.mainloop()
        return self.table


class NumberTableGUIM3:
    ''' Table of laboratory vernier caliper measurements. '''
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Number Table")
        self.table = []  # Holds rows of three columns each

        # Create widgets
        self.label = tk.Label(
            self.root, 
            text="Enter three numbers separated by spaces (e.g., '12.5 14.8 16.2'):"
        )
        self.entry = tk.Entry(self.root)
        self.add_button = tk.Button(self.root, text="Add Row", command=self.add_row)
        self.subtract_button = tk.Button(self.root, text="Remove Last Row", command=self.subtract_row)
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_matrix)
        self.matrix_label = tk.Label(self.root, text="Measurements (columns: da, db, dc):")

        # Grid layout
        self.label.grid(row=0, column=0, columnspan=2, pady=5)
        self.entry.grid(row=1, column=0, columnspan=2, pady=5)
        self.add_button.grid(row=2, column=0, pady=5)
        self.subtract_button.grid(row=2, column=1, pady=5)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=5)
        self.matrix_label.grid(row=4, column=0, columnspan=2, pady=5)

    def add_row(self):
        """ Add a new row to the table based on user input """
        row_values = self.entry.get().strip().split()  # Split input by spaces
        if len(row_values) == 3:  # Ensure exactly 3 values are entered
            try:
                self.table.append([float(val) for val in row_values])
                self.update_matrix_label()
                self.entry.delete(0, tk.END)  # Clear input field
            except ValueError:
                print("Invalid input. Please enter numeric values.")
        else:
            print("Please enter exactly 3 values for each row.")

    def subtract_row(self):
        """ Remove the last row from the table """
        if self.table:
            self.table.pop()
            self.update_matrix_label()
        else:
            print("No rows to remove.")

    def submit_matrix(self):
        """ Submit the matrix and close the window """
        print("Submitted Matrix:", self.table)
        self.root.quit()  # Exit the main loop
        self.root.destroy()  # Close the window

    def update_matrix_label(self):
        """ Update the display of the matrix of measurements """
        # Format rows for display
        matrix_text = "\n".join([f"{row[0]:.2f}  {row[1]:.2f}  {row[2]:.2f}" for row in self.table])
        self.matrix_label.config(text=f"Measurements (columns: da, db, dc):\n{matrix_text}")

    def run(self):
        """ Start the GUI main loop """
        self.root.mainloop()
        return self.table

class OffsetInputs:
    def __init__(self, length):
        self.length = length
        self.values = [0] * length
        self.sign = 1

    def run(self):
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        input_offsets = messagebox.askyesno("Input Offsets", "Were offsets recorded? Do you want to input them?")
        if not input_offsets:
            root.destroy()
            return self.values, self.sign

        root.deiconify()
        root.title("Offset Inputs")

        entries = [tk.Entry(root) for _ in range(self.length)]

        for i, entry in enumerate(entries):
            tk.Label(root, text=f"Value {i+1} (in µm):").grid(row=i, column=0)
            entry.grid(row=i, column=1)
            entry.insert(0, "0")

        sign_var = tk.StringVar(value="+")
        tk.Radiobutton(root, text="+", variable=sign_var, value="+").grid(row=self.length, column=0)
        tk.Radiobutton(root, text="-", variable=sign_var, value="-").grid(row=self.length, column=1)

        def submit():
            try:
                self.values = [float(entry.get()) for entry in entries]
                self.sign = 1 if sign_var.get() == "+" else -1
                root.quit()
                root.destroy()
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers.")

        submit_button = tk.Button(root, text="Submit", command=submit)
        submit_button.grid(row=self.length + 1, column=0, columnspan=2)

        root.mainloop()
        return self.values, self.sign