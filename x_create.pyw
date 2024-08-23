import os
import subprocess
import sys
import time

def contains_xex_or_xbe(directory):
    """Check if a directory contains any .xex or .xbe files."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xex') or file.endswith('.xbe'):
                return True
    return False

def process_files_in_directory(directory):
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
        
        sys.stdout.write(f"\rPROCESSING FILE: {file_name} \n[{progress_bar}] {i}/{total_files} ({percent_complete:.2f}%)")
        sys.stdout.flush()
        
        # Simulate processing time
        time.sleep(0.2)  # Simulate some processing delay

def create_xiso_from_directories():
    print("Batch XISO Creation v1.0\n")
    print("BY: BLAHPR 2024\n")
    print("CREATING xISO FILES FROM DIRECTORIES...\n")

    all_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and contains_xex_or_xbe(d)]
    total_dirs = len(all_dirs)

    if total_dirs == 0:
        print("NO FOLDER DIRECTORIES WITH  .xex or .xbe FILES FOUND.")
        return

    print(f"FOUND {total_dirs} FOLDER DIRECTORIES TO PROCESS.\n")

    for i, dir_name in enumerate(all_dirs, start=1):
        iso_filename = f"{dir_name}.iso"
        
        if os.path.isfile(iso_filename):
            print(f"SKIPPING: \n>FILE EXISTS<> {iso_filename}: >FILE EXISTS<")
            continue

        print(f"CREATING xISO FROM FOLDER DIRECTORY: \n{dir_name}")

        # Show progress for files in the current directory
        process_files_in_directory(dir_name)

        # Run the command to create the ISO
        result = subprocess.run(["x_tool/extract-xiso.exe", "-c", dir_name, iso_filename], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"\nError CREATING xISO for \n{dir_name}\n")
            print(f"\nCommand output: \n{result.stdout}\n")
            print(f"\nCommand error: \n{result.stderr}\n")
        else:
            print(f"SUCCESS: \n{iso_filename}\n")

    print("\nALL DONE COMPLETE.\n")
    input("Press Enter to continue...")

if __name__ == "__main__":
    create_xiso_from_directories()
