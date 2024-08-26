import os
import subprocess

def extract_xiso_from_files(delete_after=False):
    # Specify the ISO folder
    iso_folder = "x_ISO"
    
    print(f"READING FOLDER: '{iso_folder}'...")

    # List all .iso files in the ISO folder
    iso_files = [f for f in os.listdir(iso_folder) if f.endswith('.iso')]

    for iso_file in iso_files:
        print(f"\nEXTRACTING: {iso_file}\n")

        # Run the extraction command
        iso_path = os.path.join(iso_folder, iso_file)
        result = subprocess.run(
            ["x_tool/extract-xiso.exe", "-x", iso_path],
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW  # Hide the console window
        )
        
        iso_name = os.path.splitext(iso_file)[0]  # Remove the .iso extension

        if result.returncode != 0:
            print(f"SKIPPING: \nFOLDER EXISTS> {iso_name}")
        else:
            print(f"SUCCESS: \n{iso_name}")

            # Delete the ISO file if the option is selected
            if delete_after:
                print(f"\nDELETING: \n{iso_file}")
                os.remove(iso_path)

    print("\nDONE.\n")
