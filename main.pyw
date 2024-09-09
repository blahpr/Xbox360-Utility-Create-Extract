import tkinter as tk  # Standard Python interface to the Tk GUI toolkit
from tkinter import scrolledtext, Menu  # Scrollable text widget and Menu from tkinter
import threading  # Support for threading (concurrent execution)
import x_create  # Custom module for creating files, folders, or objects
import x_extract  # Custom module for extracting data or files
import sys  # Provides access to system-specific parameters and functions
import os  # OS-dependent functionality (file system operations)
import subprocess  # Running new applications or processes
import pyautogui  # Control mouse and keyboard programmatically
import time  # Time-related functions
import shutil  # High-level operations on files and directories (e.g., deletion)
import json  # For saving and loading language settings
from translations import get_translations  # Import the function from translations.py

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
        self.root.title("360 Utility Batch Create Extract v1.2")
        self.root.geometry("600x738")
        self.root.configure(bg="brown")

        # Define the x_tool folder path
        self.config_folder = os.path.join(os.getcwd(), 'x_tool')
        self.language_settings_path = os.path.join(self.config_folder, 'language_settings.json')

        # Ensure the folder exists
        os.makedirs(self.config_folder, exist_ok=True)

        # Load language from file or use default
        self.language = self.load_language()  # This will load from JSON, or default to English if not found

        self.translations = get_translations()  # Use the imported function
        self.update_language_menu_label()  # Ensure the menu label is correct initially

        # Set the icon for the Tkinter window
        icon_path = self.resource_path('images/360.ico')
        self.root.iconbitmap(icon_path)

        # Create the main layout
        self.create_widgets()

        # Initialize language setting (default is loaded language)
        self.update_texts()  # Initialize texts

        # Redirect standard output to the status window
        self.original_stdout = sys.stdout
        sys.stdout = self

        # Load configuration (no need to re-load the language here if it's done above)
        config = self.load_config()
        if "language" in config:
            self.language = config["language"]
        self.update_texts()

    def initialize_ui(self):
        # Initialize UI elements and set default language
        self.help_button = self.create_button()
        self.title_label = self.create_label()
        self.author_label = self.create_label()
        self.extract_button = self.create_button()
        self.create_button = self.create_button()

        # Set initial language settings
        self.update_language(self.language)

    def update_translated_status(self, message_key, *args):
        """ Update the status text window with a translated message. """
        # Get the translations for the current language
        tr = self.translations.get(self.language, self.translations["English"])       
        # Retrieve the translated message using the provided key
        message_template = tr.get(message_key, message_key)  # Default to key if not found  
        # Format the message with any additional arguments
        message = message_template.format(*args)        
        # Call the existing update_status method with the translated message
        self.update_status(message)

    def save_language(self):
        """ Save the selected language to the x_tool folder. """
        with open(self.language_settings_path, "w") as file:
            json.dump({"language": self.language}, file)

    def load_language(self):
        """ Load the selected language from the x_tool folder. """
        if os.path.exists(self.language_settings_path):
            with open(self.language_settings_path, "r") as file:
                data = json.load(file)
                return data.get("language", "English")
        return "English"

    def load_config(self):
        """ Load the application configuration from a JSON file. """
        if os.path.exists(self.language_settings_path):
            with open(self.language_settings_path, "r") as file:
                return json.load(file)
        return {}

    def resource_path(self, relative_path):
        """ Return the absolute path to a resource. """
        import os
        import sys
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def set_language(self, lang):
        # Update GUI text based on the selected language
        self.language = lang
        self.save_language()  # Save the selected language
        self.update_texts()  # Update all text in the GUI

        # Update the language menu label
        self.update_language_menu_label()

    def update_texts(self):
        # Update all text elements in the GUI based on the current language
        # Get the translations for the selected language, or fall back to English if not available
        tr = self.translations.get(self.language, self.translations["English"])
        
        # Update window title
        self.root.title(tr.get('title', "360 Utility Batch Create Extract v1.2"))
        
        # Update labels and buttons
        self.title_label.config(text=tr.get("title", "360 Utility Batch Create Extract v1.2"))
        self.author_label.config(text=tr.get("author", "BY: BLAHPR 2024"))
        self.extract_btn.config(text=tr.get("extract", "Extract Game Folders from ISOS"))
        self.create_btn.config(text=tr.get("create", "Create ISOS from Game Folders"))
        self.extract_delete_btn.config(text=tr.get("extract_delete", "Extract and Delete ISO Files  !!! >PERMANENTLY< !!!"))
        self.delete_source_folders_btn.config(text=tr.get("delete", "Delete Game Folders  !!! >PERMANENTLY< !!!"))
        self.fix_iso_btn.config(text=tr.get("fix_iso", "360mpGui v1.5.0.0 (Fix ISOS One by One)"))
        self.isotogod_btn.config(text=tr.get("iso2god", "ISO to GOD (GAMES ON DEMAND)"))
        self.godtoiso_btn.config(text=tr.get("god2iso", "GOD to ISO (GAMES ON DEMAND)"))
        self.image_browser_btn.config(text=tr.get("image_browser", "Xbox Image Browser"))
        self.help_btn.config(text=tr.get('help', ">Help / ReadMe<"))

        # Update language menu label
        self.update_language_menu_label()

    def update_language_menu_label(self):
        # Update the language menu label in the menubar
        if hasattr(self, 'language_menu'):
            self.menubar.entryconfig(1, label=f"{self.language}")  # Update language menu label
    
    def create_widgets(self):
        # Create menu bar
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        self.menubar = menubar

        # Language menu
        language_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=f"{self.language}", menu=language_menu)
        self.language_menu = language_menu
        languages = ["العربية (Arabic)", "中文 (Chinese)", "Nederlands (Dutch)", "English", "Français (French)", "Deutsch (German)", "हिन्दी (Hindi)", "Italiano (Italian)", "日本語 (Japanese)", "한국어 (Korean)", "Norsk (Norwegian)", "فارسی (Persian)", "Polski (Polish)", "ਪੰਜਾਬੀ (Punjabi)", "Русский (Russian)", "Español (Spanish)", "Svenska (Swedish)", "Українська (Ukrainian)"]

        for lang in languages:
            language_menu.add_command(label=lang, command=lambda l=lang: self.set_language(l))

        # Title and author labels at the top
        self.title_label = tk.Label(self.root, text="360 Utility Batch Create Extract v1.2", font=("Helvetica", 16), fg="gold", bg="brown")
        self.title_label.pack(pady=10)

        self.author_label = tk.Label(self.root, text="BY: BLAHPR 2024", font=("Helvetica", 12), fg="gold", bg="brown")
        self.author_label.pack(pady=1)

        # Buttons arranged in the middle
        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(pady=10, fill=tk.X)

        # Define a font variable for bold text
        bold_font = ("Helvetica", 12, "bold")

        self.extract_btn = tk.Button(button_frame, text="Extract Game Folders from ISOS", command=self.extract_xiso, bg="lightblue", fg="blue", font=bold_font)
        self.extract_btn.pack(pady=5, fill=tk.X, padx=20)

        self.create_btn = tk.Button(button_frame, text="Create ISOS from Game Folders", command=self.create_xiso, bg="lightgreen", fg="green", font=bold_font)
        self.create_btn.pack(pady=5, fill=tk.X, padx=20)

        self.extract_delete_btn = tk.Button(button_frame, text="Extract and Delete ISO Files  !!! >PERMANENTLY< !!!", command=self.extract_delete_xiso, bg="#FF0000", fg="yellow", font=bold_font)
        self.extract_delete_btn.pack(pady=5, fill=tk.X, padx=20)

        # New button to delete source folders
        self.delete_source_folders_btn = tk.Button(button_frame, text="Delete Game Folders  !!! >PERMANENTLY< !!!", command=self.delete_source_folders, bg="#FF0000", fg="yellow", font=bold_font)
        self.delete_source_folders_btn.pack(pady=5, fill=tk.X, padx=20)

        # New buttons to run external programs
        self.fix_iso_btn = tk.Button(button_frame, text="360mpGui v1.5.0.0 (Fix ISOS One by One)", command=self.run_external_program_1, bg="#00569D", fg="darkorange", font=bold_font)
        self.fix_iso_btn.pack(pady=5, fill=tk.X, padx=20)

        self.isotogod_btn = tk.Button(button_frame, text="ISO to GOD (GAMES ON DEMAND)", command=self.run_external_program_2, bg="#00569D", fg="darkorange", font=bold_font)
        self.isotogod_btn.pack(pady=5, fill=tk.X, padx=20)

        self.godtoiso_btn = tk.Button(button_frame, text="GOD to ISO (GAMES ON DEMAND)", command=self.run_external_program_3, bg="#00569D", fg="darkorange", font=bold_font)
        self.godtoiso_btn.pack(pady=5, fill=tk.X, padx=20)

        self.image_browser_btn = tk.Button(button_frame, text="Xbox Image Browser", command=self.run_external_program_4, bg="#00569D", fg="darkorange", font=bold_font)
        self.image_browser_btn.pack(pady=5, fill=tk.X, padx=20)

        self.help_btn = tk.Button(button_frame, text=">Help / ReadMe<", command=self.show_help, bg="crimson", fg="white", font=bold_font)
        self.help_btn.pack(pady=5, fill=tk.X, padx=20)

        # Status window at the bottom
        status_frame = tk.Frame(self.root, bg="black")
        status_frame.pack(expand=True, fill=tk.BOTH, pady=10, padx=20)

        self.status_text = tk.Text(status_frame, bg="black", fg="white", wrap=tk.WORD)
        self.status_text.pack(expand=True, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(status_frame, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)

        # Add help content display area
        self.help_text_area = tk.Text(self.root, bg="lightgrey", fg="black", wrap=tk.WORD, height=15)
        self.help_text_area.pack(pady=10, padx=10, fill=tk.BOTH)
        self.help_text_area.config(state=tk.DISABLED)

    def show_help(self):
        help_text = {
            "English": "Help content for English...",  # English
            "Español": "Contenido de ayuda en español...",  # Spanish
            "Русский": "Содержимое справки на русском...",  # Russian
            "中文": "帮助内容（中文）...",  # Chinese
            "日本語": "ヘルプ内容（日本語）..."  # Japanese
        }
        # Get the help text and title from the translations based on the selected language
        tr = self.translations.get(self.language, self.translations["English"])
        content = tr.get('help_text', self.translations["English"].get('help_text', "Help content not available."))
        self.display_text(content, tr.get("help", ">Help / ReadMe<"))
        
        # Display the help text in a new window
        self.display_text(content, title)

    def display_text(self, content, title):
        window = tk.Toplevel(self.root)
        window.title(title)
        text_area = tk.Text(window, wrap=tk.WORD)
        text_area.insert(tk.END, content)
        text_area.pack(padx=10, pady=10)
        text_area.config(state=tk.DISABLED)

    def clear_status(self):
        """ Clear the status text window. """
        self.status_text.delete('1.0', tk.END)

    def create_xiso(self):
        self.clear_status()
        threading.Thread(target=self.run_create_xiso).start()

    def run_create_xiso(self):
        x_create.create_xiso_from_directories()

    def extract_xiso(self):
        self.clear_status()
        threading.Thread(target=self.run_extract_xiso, args=(False,)).start()

    def extract_delete_xiso(self):
        self.clear_status()
        threading.Thread(target=self.run_extract_xiso, args=(True,)).start()

    def run_extract_xiso(self, delete_after):
        x_extract.extract_xiso_from_files(delete_after)

    def update_status(self, message):
        """ Update the status text window with a message. """
        # Ensure the message does not repeat if already present
        if not self.status_text.get('1.0', tk.END).strip().endswith(message.strip()):
            self.status_text.insert(tk.END, message + "\n")          
            
    def write(self, message):
        self.status_text.insert(tk.END, message)
        self.status_text.see(tk.END)

    def flush(self):
        pass

    def update_language(self, language_code):
        """ Update the language settings for the application. """
        self.language = language_code
        self.update_help_button_label()
        self.update_ui_elements()

    def update_help_button_label(self):
        """ Update the label of the Help / ReadMe button based on the selected language. """
        tr = self.translations.get(self.language, self.translations["English"])
        help_button_label = tr.get("help", ">Help / ReadMe<")
        self.help_button.set_text(help_button_label)

    def update_ui_elements(self):
        """ Update UI elements to reflect the selected language. """
        tr = self.translations.get(self.language, self.translations["English"])
        self.title_label.set_text(tr.get("title", "Default Title"))
        self.author_label.set_text(tr.get("author", "Default Author"))
        self.extract_button.set_text(tr.get("extract", "Extract"))
        self.create_button.set_text(tr.get("create", "Create"))

    def update_language(self):
        # Update the language menu to reflect the currently selected language
        if hasattr(self, 'language_menu'):
            self.language_menu.entryconfig(f"{self.language}")

    def show_help(self):
        # Create a new help window
        help_window = tk.Toplevel(self.root)
        help_window.title(">Help / ReadMe<")
        help_window.geometry("760x825")  # Set the size of the window
        help_window.configure(bg="brown")

        # Set the icon for the help window
        help_window.iconbitmap(self.resource_path('images/360.ico'))

        # Create a text widget for displaying help content
        text_widget = tk.Text(help_window, bg="lightgrey", fg="black", wrap=tk.WORD, font=("Helvetica", 13, "bold"))
        text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Add scrollbars to the text widget
        scrollbar_y = tk.Scrollbar(help_window, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar_y.set)

        scrollbar_x = tk.Scrollbar(help_window, orient=tk.HORIZONTAL, command=text_widget.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        text_widget.config(xscrollcommand=scrollbar_x.set)

        # Retrieve the help text based on the selected language
        tr = self.translations.get(self.language, self.translations["English"])
        content = tr.get('help_text', self.translations["English"].get('help_text', "Help content not available."))

        # Insert the help text into the text widget
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)  # Make the text widget read-only

    def run_external_program_1(self):
        self.clear_status()
        self.update_status("BY: 360mpGui Team")
        self.update_status("RUNNING 360mpGui v1.5.0.0.exe\n\nWAIT...\nAutomatically Opens the Utility to Browse for ISOs to Fix.\n\nWAIT...\nTry Not to Move the Mouse.")
        threading.Thread(target=self.execute_external_program_1).start()

    def execute_external_program_1(self):
        # Start the external program without a console window
        subprocess.Popen([r'x_tool\360 mp Gui v1.5.0.0\360mpGui v1.5.0.0.exe'], creationflags=subprocess.CREATE_NO_WINDOW)
        
        # Wait for the program to load
        time.sleep(4.5)
        
        # Simulate mouse clicks and keystrokes
        pyautogui.click(x=1060, y=608)  # Click OK on Error Message About no Drive Detected
        pyautogui.press('enter')        # Press Enter Key
        pyautogui.click(x=843, y=361)   # Click Create ISO Tab
        pyautogui.click(x=982, y=702)   # Click Convert an created ISO Button

        self.update_status("\nBrowse/Locate ISOS to Fix One at a Time.\nFind Window Again:\nCreate ISO <- Tab\nConvert an created ISO <- Button")

    def run_external_program_2(self):
        self.clear_status()
        self.update_status("BY: Iso2God Team")
        self.update_status("RUNNING: Iso2God.exe\n\n")
        threading.Thread(target=self.execute_external_program_2).start()

    def execute_external_program_2(self):
        # Start the external program without a console window
        subprocess.Popen([r'x_tool\iso2god-v1.3.8\Iso2God.exe'], creationflags=subprocess.CREATE_NO_WINDOW)

        # Update status message with the correct information
        self.update_status("\nCreate GOD from ISOS for Xbox360. Also Works with Original Xbox ISOS and Makes These Original Xbox Games\\ISOS GOD Format for Xbox360.")

    def run_external_program_3(self):
        self.clear_status()
        self.update_status("BY: God2Iso Team")
        self.update_status("RUNNING: God2Iso.exe")
        threading.Thread(target=self.execute_external_program_3).start()

    def execute_external_program_3(self):
        # Start the external program without a console window
        subprocess.Popen([r'x_tool\God2Iso 1.0.5\God2Iso.exe'], creationflags=subprocess.CREATE_NO_WINDOW)

        # Update status message with the correct information
        self.update_status("\nCreate ISOS from GOD 'Games on Demand' for Xbox360.\nUse 360mpGui v1.5.0.0 (Fix ISOS One by One) To Fix ISOS to Work with Xbox Image Browser.\n\nDONT FORGET:\nAfter or Before Adding ISOS Check Fix''CreateIsoGood''broken header if Needed.")

    def run_external_program_4(self):
        self.clear_status()
        self.update_status("BY: Redline99")
        self.update_status("RUNNING: Xbox Image Browser.exe")
        threading.Thread(target=self.execute_external_program_4).start()

    def execute_external_program_4(self):
        # Start the external program without a console window
        subprocess.Popen([r'x_tool\360 mp Gui v1.5.0.0\360mpTools\Xbox Image Browser.exe'], creationflags=subprocess.CREATE_NO_WINDOW)

        # Update status message with the correct information
        self.update_status("\nGetting Error Running Xbox Image Browser.\n\nOpen As Admin >Run As Admin MSCOMCTL.OCX.bat< From\nx_tool\\360 mp Gui v1.5.0.0\\360mpTools\\RunAsAdmin MSCOMCTL.OCX.bat\n\nThis Will Register MSCOMCTL.OCX for Windows\n\nPress OK and Try to Open\\Run Again.")

    def delete_source_folders(self):
        self.clear_status()
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))  # Get directory of the executable
        
        # Exclude specific folders
        excluded_folders = ["x_tool", "x_ISO"]
        
        # Flag to check if any folder was deleted
        deleted_any_folders = False
        
        for folder_name in os.listdir(base_dir):
            folder_path = os.path.join(base_dir, folder_name)
            
            # Check if it's a directory and not in the excluded list
            if os.path.isdir(folder_path) and folder_name not in excluded_folders:
                # Check if the folder contains .xex or .xbe files
                contains_target_files = any(
                    filename.endswith(('.xex', '.xbe')) for filename in os.listdir(folder_path)
                )
                
                if contains_target_files:
                    try:
                        shutil.rmtree(folder_path)  # Remove the folder and all its contents
                        self.update_status(f"\nDELETING: \n{folder_name}\n")
                        self.update_status("DONE.")
                        deleted_any_folders = True
                    except Exception as e:
                        self.update_status(f"\nFailed to delete folder {folder_name}: {e}\n")
        
        # Check if no folders were deleted
        if not deleted_any_folders:
            self.update_status("\nNO GAME FOLDERS TO DELETE")
        else:
            self.update_status("DONE.")
    
def main():
    root = tk.Tk()
    app = XISOToolApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
