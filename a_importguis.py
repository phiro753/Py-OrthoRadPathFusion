# Classes for import guis
# Robert Phillips
# Created 2024-06-21

import tkinter as tk
from tkinter import filedialog
import os

class StringReturn:
    ''' Asking the user what bisection this is '''
    ''' Need to differentiate between histology assignment planes for different bisections if exporting to file '''
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('User Input')

        # Create a label
        self.label = tk.Label(self.root, text="A short filename suffix for which biseciton this is (e.g. M or L for Medial or Lateral)")
        self.label.pack()

        # Create an entry widget
        self.entry = tk.Entry(self.root)
        self.entry.pack()
        self.entry.focus_set()

        self.user_input = None

        # building the okay button position and what it does into the gui window
        self.ok_button = tk.Button(self.root, text='Okay', command=self.get_input_and_close) 
        self.ok_button.pack(side='bottom')

        # Bind the Enter key to the same function
        self.root.bind('<Return>', lambda event: self.get_input_and_close())

    def get_input_and_close(self):
        self.user_input = self.entry.get()
        # print("User input:", self.user_input)
        self.root.destroy()  # Close the window

    def run(self):
        self.root.mainloop()
        return self.user_input

class FileSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main tkinter window

    def show_message(self, message):
        """
        Displays a message in a GUI window.
        """
        tk.messagebox.showinfo("Message", message)

    def select_file(self):
        """
        Opens a file dialog to choose a file.
        Returns the full path of the selected file.
        """
        initial_dir = os.path.dirname(os.path.realpath(__file__))  # Get the current directory of the Python file
        file_path = filedialog.askopenfilename(initialdir=initial_dir)
        return file_path

class OutputDecision:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Yes or No")
        self.output_directory = None

        # Create label with the message
        self.message_label = tk.Label(self.root, text='Actually, do you even want planes to be saved to a folder?')
        self.message_label.pack()

        # Create buttons
        self.yes_button = tk.Button(self.root, text="Yes", command=self.handle_yes)
        self.no_button = tk.Button(self.root, text="No", command=self.handle_no)
        
        # Pack buttons
        self.yes_button.pack(side="left", padx=10)
        self.no_button.pack(side="right", padx=10)

    def handle_yes(self):
        initial_dir = os.path.dirname(os.path.realpath(__file__))  # Get the current directory of the Python file
        self.output_directory = filedialog.askdirectory(initialdir=initial_dir)
        self.root.quit()  # Exit the main loop

    def handle_no(self):
        self.root.quit()  # Exit the main loop

    def run(self): 
        self.root.mainloop()
        self.root.destroy()  # Ensure the window is properly destroyed
        return self.output_directory


class NumberTableGUI:
    '''Table of labrotory vernier caliper measurements.'''
    '''These  should have been taken from the fiducial reference to the bandsawed/cut dissection block face edge that has been modelled with splines from 3DSlicer'''
    def __init__(self):
        # self.root = root
        self.root = tk.Tk()
        self.root.title("Number Table")
        self.table = []

        # Create widgets
        self.label = tk.Label(self.root, text="Enter two numbers separated by a space:")
        self.entry = tk.Entry(self.root)
        self.add_button = tk.Button(self.root, text="Add Row", command=self.add_row)
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_matrix)
        self.subtract_button = tk.Button(self.root, text="Subtract Row", command=self.subtract_row)
        self.matrix_label = tk.Label(self.root, text="Measurements pairs:")

        # Grid layout
        self.label.grid(row=0, column=0, columnspan=2)
        self.entry.grid(row=1, column=0, columnspan=2)
        self.add_button.grid(row=2, column=0, columnspan=2)
        self.subtract_button.grid(row=3, column=0, columnspan=2)
        self.submit_button.grid(row=4, column=0, columnspan=2)
        self.matrix_label.grid(row=5, column=0, columnspan=2)

        # Start the main loop
        self.root.mainloop()

    def add_row(self):
        row_values = self.entry.get().replace(',', ' ').split() # user can use ' ' or ',' or both to separate measurement values
        if len(row_values) == 2:
            self.table.append([float(val) for val in row_values])
            self.update_matrix_label()
            self.entry.delete(0, tk.END)  # Clear the input box after adding row
        else:
            print("Please enter exactly 2 values for each row.")

    def subtract_row(self):
        '''functionality to subtract a row'''
        if self.table:
            self.table.pop()
            self.update_matrix_label()
        else:
            print("No rows to remove.")

    def submit_matrix(self):
        # Close the GUI window
        self.root.destroy()


    def update_matrix_label(self):
        matrix_text = "\n".join([f"{row[0]:.2f}  {row[1]:.2f}" for row in self.table])
        self.matrix_label.config(text=f"Measurements pairs (da and db respectively):\n{matrix_text}")

    
class OffsetInputs:
    def __init__(self, length):
        self.length = length
        self.values = [0] * length # create array of offset by 0 as default
        self.sign = 1

    def get_offsets(self):
        # First asking user if they would like to input offset values
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        # Ask if the user wants to input offsets
        input_offsets = tk.messagebox.askyesno("Input Offsets", "Were offsets recorded/do you want to input them?")
        if not input_offsets: # if user doesn't want to, use default offsets of 0
            root.destroy() 
            self.sign = 1 # default sign is positive ('+') out of convention
            return self.values, self.sign # return early

        root.deiconify()  # Show the root window
        root.title("Offset Inputs")

        def submit():
            try:
                self.values = [float(entry.get()) for entry in entries]
                self.sign = 1 if sign_var.get() == '+' else -1
                root.destroy()
            except ValueError:
                tk.messagebox.showerror("Input Error", "Please enter valid numbers.")


        entries = [tk.Entry(root) for _ in range(self.length)]
        for i, entry in enumerate(entries):
            tk.Label(root, text=f"Value {i+1} (in um):").grid(row=i, column=0)
            entry.grid(row=i, column=1)
            entry.insert(0, '0')  # Prepopulate offsets in cells with 0

        '''creating sign at bottom of window for specification if microtomb offsets are subtracted off ('-'), or added to dissection blockface (often this will be '-' as microtombing will be taken off face measured with caliper too)'''
        sign_var = tk.StringVar(value='+') 
        tk.Radiobutton(root, text='+', variable=sign_var, value='+').grid(row=self.length, column=0)
        tk.Radiobutton(root, text='-', variable=sign_var, value='-').grid(row=self.length, column=1)

        tk.Button(root, text="Submit", command=submit).grid(row=self.length + 1, columnspan=2)

        root.mainloop()

        return self.values, self.sign