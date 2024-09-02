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

        self.translations = self.get_translations()  # Dictionary of translations

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

    def get_translations(self):
        """ Dictionary of translations for the GUI. """
        return { # English
            "English": {
                "title": "360 Utility Batch Create Extract v1.2",
                "author": "BY: BLAHPR 2024",
                "extract": "Extract Game Folders from ISOS",
                "create": "Create ISOS from Game Folders",
                "extract_delete": "Extract and Delete ISO Files  !!! >PERMANENTLY< !!!",
                "delete": "Delete Game Folders  !!! >PERMANENTLY< !!!",
                "fix_iso": "Fix ISOS One by One",
                "iso2god": "ISO to GOD (GAMES ON DEMAND)",
                "god2iso": "GOD to ISO (GAMES ON DEMAND)",
                "image_browser": "Xbox Image Browser",
                "help": ">Help / ReadMe<",
                'help_text': (
                    "* 360 Utility Batch Create Extract\n\n"
                    "* Batch Extraction and Creation of Xbox 360 and Original Xbox ISOs\n\n"
                    "* This setup allows you to efficiently manage multiple ISOs at once, with\n"
                    "* all extracted and created files organized next to the x_ISO folder.\n\n"
                    "**********************************************************************\n"
                    "1.. Batch Extraction of ISOs:\n\n"
                    "* Place your ISO files into folder named x_ISO.\n\n"
                    "* This Utility will batch-extract games from these ISO files.\n\n"
                    "* The extracted game folders will be created next to the x_ISO folder and\n"
                    "* contain xex or xbe, not inside ISO folder.\n\n"
                    "**********************************************************************\n"
                    "2.. Batch Creation of ISOs From Game Folders:\n\n"
                    "* Ensure that the game folders are placed next to the x_ISO folder, not\n"
                    "* inside it.\n\n"
                    "* This Utility will batch-create ISO files from these game folders that contain\n"
                    "* xex or xbe.\n\n"
                    "* The newly created ISO files will be saved next to the x_ISO folder.\n\n"
                    "**********************************************************************\n"
                    "* 8/19/2024 8:12 PM\n\n"
                    "* BLAHPR 2024.\n\n"
                    "* Contact Email: geebob273@gmail.com\n\n"
                    "                                                ~~> Credits's <~~\n"
                    "                                                       **********\n"
                    "                     <in@fishtank.com> for your cool work and source code.\n"
                ),
            }, # Spanish
            "Español": {
                "title": "360 Utility Crear y Extraer por Lote v1.2",
                "author": "POR: BLAHPR 2024",
                "extract": "Extraer Carpetas de Juegos de ISOS",
                "create": "Crear ISOS de Carpetas de Juegos",
                "extract_delete": "Extraer y Eliminar Archivos ISO  !!! >PERMANENTE< !!!",
                "delete": "Eliminar Carpetas de Juegos  !!! >PERMANENTE< !!!",
                "fix_iso": "Arreglar ISOS Uno por Uno",
                "iso2god": "ISO a GOD (JUEGOS BAJO DEMANDA)",
                "god2iso": "GOD a ISO (JUEGOS BAJO DEMANDA)",
                "image_browser": "Explorador de Imágenes de Xbox",
                "help": ">Ayuda / LeerMe<",
                'help_text': (
                    "* 360 Utility Crear y Extraer en Lote\n\n"
                    "* Extracción y Creación en Lote de ISOs de Xbox 360 y Xbox Original\n\n"
                    "* Esta configuración te permite gestionar múltiples ISOs a la vez, con\n"
                    "* todos los archivos extraídos y creados organizados junto a la carpeta x_ISO.\n\n"
                    "**********************************************************************\n"
                    "1.. Extracción en Lote de ISOs:\n\n"
                    "* Coloca tus archivos ISO en una carpeta llamada x_ISO.\n\n"
                    "* Esta utilidad extraerá en lote los juegos de estos archivos ISO.\n\n"
                    "* Las carpetas de juegos extraídas se crearán junto a la carpeta x_ISO y\n"
                    "* contendrán xex o xbe, no dentro de la carpeta ISO.\n\n"
                    "**********************************************************************\n"
                    "2.. Creación en Lote de ISOs Desde Carpetas de Juegos:\n\n"
                    "* Asegúrate de que las carpetas de juegos estén colocadas junto a la carpeta x_ISO, no\n"
                    "* dentro de ella.\n\n"
                    "* Esta utilidad creará en lote archivos ISO a partir de estas carpetas de juegos que contienen\n"
                    "* xex o xbe.\n\n"
                    "* Los archivos ISO recién creados se guardarán junto a la carpeta x_ISO.\n\n"
                    "**********************************************************************\n"
                    "* 19/08/2024 8:12 PM\n\n"
                    "* BLAHPR 2024.\n\n"
                    "* Correo de contacto: geebob273@gmail.com\n\n"
                    "                                                ~~> Créditos <~~\n"
                    "                                                       **********\n"
                    "                     <in@fishtank.com> por tu genial trabajo y código fuente.\n"
                ),
            }, # Russian
            "Русский": {
                "title": "360 Utility Пакетное Создание и Извлечение v1.2",
                "author": "Автор: BLAHPR 2024",
                "extract": "Извлечь Папки Игр из ISO",
                "create": "Создать ISO из Папок Игр",
                "extract_delete": "Извлечь и Удалить ISO Файлы  !!! >ПОСТОЯННО< !!!",
                "delete": "Удалить Папки Игр  !!! >ПОСТОЯННО< !!!",
                "fix_iso": "Исправить ISO по Одному",
                "iso2god": "ISO в GOD (ИГРЫ НА ТРЕБОВАНИЕ)",
                "god2iso": "GOD в ISO (ИГРЫ НА ТРЕБОВАНИЕ)",
                "image_browser": "Обозреватель Изображений Xbox",
                "help": ">Помощь / Прочитать<",
                'help_text': (
                    "* 360 Utility Пакетное Создание и Извлечение\n\n"
                    "* Пакетное Извлечение и Создание ISOs для Xbox 360 и Xbox Original\n\n"
                    "* Эта настройка позволяет эффективно управлять несколькими ISO одновременно,\n"
                    "* все извлеченные и созданные файлы организованы рядом с папкой x_ISO.\n\n"
                    "**********************************************************************\n"
                    "1.. Пакетное Извлечение ISOs:\n\n"
                    "* Поместите ваши ISO файлы в папку с именем x_ISO.\n\n"
                    "* Эта утилита будет пакетно извлекать игры из этих ISO файлов.\n\n"
                    "* Извлеченные игровые папки будут созданы рядом с папкой x_ISO и\n"
                    "* содержать xex или xbe, не внутри папки ISO.\n\n"
                    "**********************************************************************\n"
                    "2.. Пакетное Создание ISOs из Игровых Папок:\n\n"
                    "* Убедитесь, что игровые папки находятся рядом с папкой x_ISO, а не\n"
                    "* внутри нее.\n\n"
                    "* Эта утилита будет пакетно создавать ISO файлы из этих игровых папок, содержащих\n"
                    "* xex или xbe.\n\n"
                    "* Новые ISO файлы будут сохранены рядом с папкой x_ISO.\n\n"
                    "**********************************************************************\n"
                    "* 19/08/2024 20:12\n\n"
                    "* BLAHPR 2024.\n\n"
                    "* Контактный Email: geebob273@gmail.com\n\n"
                    "                                                ~~> Кредиты <~~\n"
                    "                                                       **********\n"
                    "                     <in@fishtank.com> за вашу отличную работу и исходный код.\n"
                ),
            }, # Chinese
            "中文": {
                "title": "360 Utility 批量创建提取 v1.2",
                "author": "作者: BLAHPR 2024",
                "extract": "从ISO中提取游戏文件夹",
                "create": "从游戏文件夹创建ISO",
                "extract_delete": "提取并删除ISO文件  !!! >永久< !!!",
                "delete": "删除游戏文件夹  !!! >永久< !!!",
                "fix_iso": "逐个修复ISO",
                "iso2god": "ISO 转 GOD（按需游戏）",
                "god2iso": "GOD 转 ISO（按需游戏）",
                "image_browser": "Xbox图像浏览器",
                "help": ">帮助 / 阅读<",
                'help_text': (
                    "* 360 Utility 批量创建提取\n\n"
                    "* Xbox 360 和 Xbox 原版 ISOs 的批量提取和创建\n\n"
                    "* 此设置允许您一次高效管理多个 ISO，所有提取和创建的文件\n"
                    "* 将与 x_ISO 文件夹一起组织。\n\n"
                    "**********************************************************************\n"
                    "1.. 批量提取 ISOs:\n\n"
                    "* 将您的 ISO 文件放入名为 x_ISO 的文件夹中。\n\n"
                    "* 此工具将批量提取这些 ISO 文件中的游戏。\n\n"
                    "* 提取的游戏文件夹将创建在 x_ISO 文件夹旁边，\n"
                    "* 包含 xex 或 xbe，不在 ISO 文件夹内。\n\n"
                    "**********************************************************************\n"
                    "2.. 从游戏文件夹批量创建 ISOs:\n\n"
                    "* 确保游戏文件夹位于 x_ISO 文件夹旁边，而不是\n"
                    "* 里面。\n\n"
                    "* 此工具将从包含 xex 或 xbe 的这些游戏文件夹批量创建 ISO 文件。\n\n"
                    "* 新创建的 ISO 文件将保存到 x_ISO 文件夹旁边。\n\n"
                    "**********************************************************************\n"
                    "* 2024年8月19日 20:12\n\n"
                    "* BLAHPR 2024.\n\n"
                    "* 联系邮件: geebob273@gmail.com\n\n"
                    "                                                ~~> 版权声明 <~~\n"
                    "                                                       **********\n"
                    "                     <in@fishtank.com> 感谢您的出色工作和源代码。\n"
                ),
            }, # Japanese
            "日本語": {
                "title": "360 Utility バッチ作成抽出 v1.2",
                "author": "BY: BLAHPR 2024",
                "extract": "ISOからゲームフォルダを抽出",
                "create": "ゲームフォルダからISOを作成",
                "extract_delete": "ISOファイルを抽出して削除 !!! >永久< !!!",
                "delete": "ゲームフォルダを削除 !!! >永久< !!!",
                "fix_iso": "ISOを一つずつ修正",
                "iso2god": "ISOをGODに変換 (オンデマンドゲーム)",
                "god2iso": "GODをISOに変換 (オンデマンドゲーム)",
                "image_browser": "Xboxイメージブラウザ",
                "help": ">ヘルプ / 読み取り<",
                'help_text': (
                    "* 360 Utility バッチ作成抽出\n\n"
                    "* Xbox 360 およびオリジナル Xbox ISOs のバッチ抽出および作成\n\n"
                    "* この設定により、一度に複数の ISO を効率的に管理でき、\n"
                    "* すべての抽出および作成されたファイルが x_ISO フォルダの隣に整理されます。\n\n"
                    "**********************************************************************\n"
                    "1.. ISO のバッチ抽出:\n\n"
                    "* ISO ファイルを x_ISO という名前のフォルダに置きます。\n\n"
                    "* このユーティリティは、これらの ISO ファイルからゲームをバッチ抽出します。\n\n"
                    "* 抽出されたゲームフォルダは x_ISO フォルダの隣に作成され、\n"
                    "* ISO フォルダ内ではなく xex または xbe を含みます。\n\n"
                    "**********************************************************************\n"
                    "2.. ゲームフォルダからのバッチ ISO 作成:\n\n"
                    "* ゲームフォルダが x_ISO フォルダの隣に置かれていることを確認します。\n"
                    "* 内部ではなく。\n\n"
                    "* このユーティリティは、これらのゲームフォルダから ISO ファイルをバッチ作成します。\n"
                    "* xex または xbe を含む。\n\n"
                    "* 新しく作成された ISO ファイルは x_ISO フォルダの隣に保存されます。\n\n"
                    "**********************************************************************\n"
                    "* 2024年8月19日 20:12\n\n"
                    "* BLAHPR 2024.\n\n"
                    "* 連絡先メール: geebob273@gmail.com\n\n"
                    "                                                ~~> クレジット <~~\n"
                    "                                                       **********\n"
                    "                     <in@fishtank.com> 素晴らしい仕事とソースコードに感謝します。\n"
                ),
            },
            # Add additional languages as needed
        }

    def set_language(self, lang):
        # Update GUI text based on the selected language
        self.language = lang
        self.save_language()  # Save the selected language
        self.update_texts()  # Update all text in the GUI

        # Update the language menu label
        if hasattr(self, 'language_menu'):
            self.language_menu.entryconfig("Language", label=f"Language: {self.language}")

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
        self.fix_iso_btn.config(text=tr.get("fix_iso", "Fix ISOS One by One"))
        self.isotogod_btn.config(text=tr.get("iso2god", "ISO to GOD (GAMES ON DEMAND)"))
        self.godtoiso_btn.config(text=tr.get("god2iso", "GOD to ISO (GAMES ON DEMAND)"))
        self.image_browser_btn.config(text=tr.get("image_browser", "Xbox Image Browser"))
        self.help_btn.config(text=tr.get('help', ">Help / ReadMe<"))

        # Update language menu label
        if hasattr(self, 'language_menu'):
            self.language_menu.entryconfig("Language", label=f"Language: {self.language}")

    def save_language(self):
        """ Save the selected language to a file in the x_tool folder. """
        os.makedirs(self.config_folder, exist_ok=True)
        with open(self.language_settings_path, "w") as file:
            json.dump({"language": self.language}, file)

    def load_language(self):
        """ Load the selected language from a file in the x_tool folder. """
        if os.path.exists(self.language_settings_path):
            with open(self.language_settings_path, "r") as file:
                data = json.load(file)
                return data.get("language", "English")
        return "English"

    def create_widgets(self):
        # Create menu bar
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # Language menu
        language_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Language", menu=language_menu)
        languages = ["English", "Español", "Русский", "中文", "日本語"]
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
        self.fix_iso_btn = tk.Button(button_frame, text="Fix ISOS One by One", command=self.run_external_program_1, bg="#00569D", fg="darkorange", font=bold_font)
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
            self.language_menu.entryconfig("Language", label=f"Language: {self.language}")

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
        self.update_status("\nCreate ISOS from GOD 'Games on Demand' for Xbox360.\nUse Fix ISOS One by One To Fix ISOS to Work with Xbox Image Browser.\n\nDONT FORGET:\nAfter or Before Adding ISOS Check Fix''CreateIsoGood''broken header if Needed.")

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
