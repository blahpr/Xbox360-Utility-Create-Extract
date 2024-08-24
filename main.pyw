import tkinter as tk
from tkinter import scrolledtext
import threading
import x_create
import x_extract
import sys
import os
import subprocess
import pyautogui
import time

# Function to find resource paths when bundled with PyInstaller
def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and PyInstaller. """
    try:
        # PyInstaller creates a temporary folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class XISOToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("360 XISO Batch Create Extract v1.1")
        self.root.geometry("600x650")
        self.root.configure(bg="brown")

        # Set the icon for the Tkinter window using resource_path
        icon_path = resource_path('images/360.ico')
        self.root.iconbitmap(icon_path)

        # Create the main layout
        self.create_widgets()

        # Redirect standard output to the status window
        self.original_stdout = sys.stdout
        sys.stdout = self

    def create_widgets(self):
        # Title and author labels at the top
        title_label = tk.Label(self.root, text="360 XISO Batch Create Extract v1.1", font=("Helvetica", 16), fg="gold", bg="brown")
        title_label.pack(pady=10)

        author_label = tk.Label(self.root, text="BY: BLAHPR 2024", font=("Helvetica", 12), fg="gold", bg="brown")
        author_label.pack(pady=1)

        # Buttons arranged in the middle
        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(pady=10, fill=tk.X)

        # Define a font variable for bold text
        bold_font = ("Helvetica", 12, "bold")

        create_btn = tk.Button(button_frame, text="CREATE xISO's FROM FOLDER DIRECTORIE'S", command=self.create_xiso, bg="lightgreen", fg="green", font=bold_font)
        create_btn.pack(pady=5, fill=tk.X, padx=20)

        extract_btn = tk.Button(button_frame, text="EXTRACT xISO's TO FOLDER DIRECTORIE'S", command=self.extract_xiso, bg="lightblue", fg="blue", font=bold_font)
        extract_btn.pack(pady=5, fill=tk.X, padx=20)

        extract_delete_btn = tk.Button(button_frame, text="EXTRACT AND PERMANENTLY DELETE xISO FILE'S", command=self.extract_delete_xiso, bg="#FF0000", fg="yellow", font=bold_font)
        extract_delete_btn.pack(pady=5, fill=tk.X, padx=20)

        # New button to run the external program
        fix_iso_btn = tk.Button(button_frame, text="FIX ISO's ONE at A Time", command=self.run_external_program, bg="#00569D", fg="darkorange", font=bold_font)
        fix_iso_btn.pack(pady=5, fill=tk.X, padx=20)

        help_btn = tk.Button(button_frame, text=">>HELP \\ READ ME<<", command=self.show_help, bg="crimson", fg="white", font=bold_font)
        help_btn.pack(pady=5, fill=tk.X, padx=20)

        # Status window at the bottom
        status_frame = tk.Frame(self.root, bg="black")
        status_frame.pack(expand=True, fill=tk.BOTH, pady=10, padx=20)

        self.status_text = tk.Text(status_frame, bg="black", fg="white", wrap=tk.WORD)
        self.status_text.pack(expand=True, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(status_frame, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)

    def clear_status(self):
        """ Clear the status text window. """
        self.status_text.delete('1.0', tk.END)

    def create_xiso(self):
        self.clear_status()
        self.update_status("\nStarting xISO creation...\n")
        threading.Thread(target=self.run_create_xiso).start()

    def run_create_xiso(self):
        x_create.create_xiso_from_directories()
        self.update_status("\nxISO creation complete.\n")

    def extract_xiso(self):
        self.clear_status()
        self.update_status("\nStarting xISO extraction...\n")
        threading.Thread(target=self.run_extract_xiso, args=(False,)).start()

    def extract_delete_xiso(self):
        self.clear_status()
        self.update_status("\nStarting xISO extraction and deletion...\n")
        threading.Thread(target=self.run_extract_xiso, args=(True,)).start()

    def run_extract_xiso(self, delete_after):
        x_extract.extract_xiso_from_files(delete_after)
        self.update_status("\nxISO extraction and deletion complete.\n")

    def update_status(self, message):
        self.status_text.insert(tk.END, message)
        self.status_text.see(tk.END)

    def write(self, message):
        self.status_text.insert(tk.END, message)
        self.status_text.see(tk.END)

    def flush(self):
        pass

    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title(">ReadMe 360 XISO Batch Create Extract v1.1<")
        help_window.geometry("800x800")
        help_window.configure(bg="brown")

        # Set the icon for the help window using resource_path
        help_window.iconbitmap(resource_path('images/360.ico'))

        text_widget = tk.Text(help_window, bg="pink", fg="purple", wrap=tk.WORD, font=("Helvetica", 16))
        text_widget.pack(expand=True, fill=tk.BOTH)

        scrollbar_y = tk.Scrollbar(help_window, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar_y.set)

        scrollbar_x = tk.Scrollbar(help_window, orient=tk.HORIZONTAL, command=text_widget.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        text_widget.config(xscrollcommand=scrollbar_x.set)

        help_text = (
            "* 360 XISO Batch Create Extract v1.1\n\n"
            "* Batch Extraction and Creation of Xbox 360 and Original Xbox ISOs\n\n"
            "* This setup allows you to efficiently manage multiple ISOs at once, with\n"
            "* all extracted and created files organized next to the x_ISO folder.\n\n"
            "**********************************************************************\n"
            "1.. Batch Extraction of ISOs:\n\n"
            "* Place your ISO files into folder named x_ISO.\n\n"
            "* The tool will batch-extract games from these ISO files.\n\n"
            "* The extracted game folders will be created next to the x_ISO folder and\n"
            "* contain xex or xbe, not inside ISO folder.\n\n"
            "**********************************************************************\n"
            "2.. Batch Creation of ISOs From Game Folders:\n\n"
            "* Ensure that the game folders are placed next to the x_ISO folder, not\n"
            "* inside it.\n\n"
            "* The tool will batch-create ISO files from these game folders that contain\n"
            "* xex or xbe.\n\n"
            "* The newly created ISO files will be saved next to the x_ISO folder.\n\n"
            "**********************************************************************\n"
            "* 8/19/2024 8:12 PM\n\n"
            "* BLAHPR 2024.\n\n"
            "* Contact Email: geebob273@gmail.com\n\n"
            "                                           ~~> THANK YOU'S <~~\n"
            "                                                  *****************\n"
            "                     <in@fishtank.com> for your cool work and source code.\n"
        )
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)

        close_btn = tk.Button(help_window, text="CLOSE", command=help_window.destroy, bg="darkgreen", fg="tan")
        close_btn.pack(pady=10)

    def run_external_program(self):
        self.clear_status()
        self.update_status("\nRUNNING 360mpGui v1.5.0.0.exe\n\n")
        threading.Thread(target=self.execute_external_program).start()

    def execute_external_program(self):
        # Start the external program without a console window
        subprocess.Popen([r'x_tool\360 mp Gui v1.5.0.0\360mpGui v1.5.0.0.exe'], creationflags=subprocess.CREATE_NO_WINDOW)
        
        # Wait for the program to load
        time.sleep(4.5)
        
        # Simulate mouse clicks and keystrokes
        pyautogui.click(x=1060, y=608)  # Click OK on Error Message About no Drive Detected
        pyautogui.press('enter')        # Press Enter Key
        pyautogui.click(x=843, y=361)   # Click Create ISO Tab
        pyautogui.click(x=982, y=702)   # Click Convert an created ISO Button

        self.update_status("\n\nBrowse \\ Locate ISO's to Fix One at a Time.\n")

def main():
    root = tk.Tk()
    app = XISOToolApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
