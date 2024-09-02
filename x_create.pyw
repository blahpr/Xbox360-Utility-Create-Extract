import os
import subprocess
import sys
import time
from threading import Thread

# Define translations
translations = {
    "English": {
        "no_folders": "NO FOLDER DIRECTORIES WITH .xex or .xbe FILES FOUND.",
        "found_folders": "FOUND {count} FOLDER DIRECTORIES TO PROCESS.\n",
        "skipping_file": "SKIPPING: \nFILE EXISTS> {filename}",
        "game_folder": "Game Folder: \n{dirname}",
        "error_creating_iso": "\nError CREATING ISO for \n{dirname}\n",
        "command_output": "\nCommand output: \n{stdout}\n",
        "command_error": "\nCommand error: \n{stderr}\n",
        "success": "SUCCESS \n{filename}\n",
        "done": "\nDONE.\n",
        "processing": "PROCESSING: {filename}",
        "progress_bar": "[{progress_bar}] {current}/{total}(%)"
    },
    "Español": {
        "no_folders": "NO SE ENCONTRARON DIRECTORIOS CON ARCHIVOS .xex o .xbe.",
        "found_folders": "ENCONTRADOS {count} DIRECTORIOS PARA PROCESAR.\n",
        "skipping_file": "SALTANDO: \nEL ARCHIVO EXISTE> {filename}",
        "game_folder": "Carpeta del juego: \n{dirname}",
        "error_creating_iso": "\nError AL CREAR ISO para \n{dirname}\n",
        "command_output": "\nSalida del comando: \n{stdout}\n",
        "command_error": "\nError del comando: \n{stderr}\n",
        "success": "ÉXITO \n{filename}\n",
        "done": "\nHECHO.\n",
        "processing": "PROCESANDO: {filename}",
        "progress_bar": "[{progress_bar}] {current}/{total}(%)"
    },
    "Русский": {
        "no_folders": "ДИРЕКТОРИИ С ФАЙЛАМИ .xex ИЛИ .xbe НЕ НАЙДЕНЫ.",
        "found_folders": "НАЙДЕНО {count} ДИРЕКТОРИЙ ДЛЯ ОБРАБОТКИ.\n",
        "skipping_file": "ПРОПУСК: \nФАЙЛ УЖЕ СУЩЕСТВУЕТ> {filename}",
        "game_folder": "Папка игры: \n{dirname}",
        "error_creating_iso": "\nОшибка СОЗДАНИЯ ISO для \n{dirname}\n",
        "command_output": "\nВывод команды: \n{stdout}\n",
        "command_error": "\nОшибка команды: \n{stderr}\n",
        "success": "УСПЕХ \n{filename}\n",
        "done": "\nГОТОВО.\n",
        "processing": "ОБРАБОТКА: {filename}",
        "progress_bar": "[{progress_bar}] {current}/{total}(%)"
    },
    "中文": {
        "no_folders": "没有包含 .xex 或 .xbe 文件的文件夹目录。",
        "found_folders": "发现 {count} 个文件夹目录进行处理。\n",
        "skipping_file": "跳过：\n文件已存在> {filename}",
        "game_folder": "游戏文件夹：\n{dirname}",
        "error_creating_iso": "\n创建 ISO 时出错 \n{dirname}\n",
        "command_output": "\n命令输出：\n{stdout}\n",
        "command_error": "\n命令错误：\n{stderr}\n",
        "success": "成功 \n{filename}\n",
        "done": "\n完成。\n",
        "processing": "处理：{filename}",
        "progress_bar": "[{progress_bar}] {current}/{total}(%)"
    },
    "日本語": {
        "no_folders": ".xex または .xbe ファイルを含むフォルダー ディレクトリが見つかりません。",
        "found_folders": "処理するフォルダー ディレクトリ {count} 件が見つかりました。\n",
        "skipping_file": "スキップ：\nファイルが既に存在します> {filename}",
        "game_folder": "ゲーム フォルダー：\n{dirname}",
        "error_creating_iso": "\nISO 作成エラー \n{dirname}\n",
        "command_output": "\nコマンドの出力：\n{stdout}\n",
        "command_error": "\nコマンドエラー：\n{stderr}\n",
        "success": "成功 \n{filename}\n",
        "done": "\n完了。\n",
        "processing": "処理中：{filename}",
        "progress_bar": "[{progress_bar}] {current}/{total}(%)"
    }
}

def get_translation(key, language):
    """Get the translation for the given language."""
    # Get the translations for the specified language, defaulting to English if not found
    lang_translations = translations.get(language, translations["English"])
    # Return the translation for the given key, defaulting to the key itself if not found
    return lang_translations.get(key, key)

def contains_xex_or_xbe(directory):
    """Check if a directory contains any .xex or .xbe files."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xex') or file.endswith('.xbe'):
                return True
    return False

def process_files_in_directory(directory, language):
    """Simulate file processing and show progress."""
    files = [f for f in os.listdir(directory) if f.endswith('.xex') or f.endswith('.xbe')]
    total_files = len(files)
    
    if total_files == 0:
        return
    
    for i, file_name in enumerate(files, start=1):
        # Simulate file processing
        progress = i / total_files
        percent_complete = int(progress * 100)
        progress_bar = '#' * int(progress * 40) + '-' * (40 - int(progress * 40))
        
        sys.stdout.write(f"\r{get_translation('processing', language).format(filename=file_name)}\n{get_translation('progress_bar', language).format(progress_bar=progress_bar, current=i, total=total_files)}")
        sys.stdout.flush()
        
        # Simulate processing time
        time.sleep(0.2)  # Simulate some processing delay

def create_xiso_from_directories(language="English"):
    all_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and contains_xex_or_xbe(d)]
    total_dirs = len(all_dirs)

    if total_dirs == 0:
        print(get_translation("no_folders", language))
        return

    print(get_translation("found_folders", language).format(count=total_dirs))

    for i, dir_name in enumerate(all_dirs, start=1):
        iso_filename = f"{dir_name}.iso"
        
        if os.path.isfile(iso_filename):
            print(get_translation("skipping_file", language).format(filename=iso_filename))
            continue

        print(get_translation("game_folder", language).format(dirname=dir_name))

        # Show progress for files in the current directory
        process_files_in_directory(dir_name, language)

        # Run the command to create the ISO
        result = subprocess.run(
            ["x_tool/extract-xiso.exe", "-c", dir_name, iso_filename],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW  # Hide the console window
        )
        
        if result.returncode != 0:
            print(get_translation("error_creating_iso", language).format(dirname=dir_name))
            print(get_translation("command_output", language).format(stdout=result.stdout))
            print(get_translation("command_error", language).format(stderr=result.stderr))
        else:
            print(get_translation("success", language).format(filename=iso_filename))

    print(get_translation("done", language))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        language = sys.argv[1]
    else:
        language = "English"  # Default language if none is passed

    create_xiso_from_directories(language)
