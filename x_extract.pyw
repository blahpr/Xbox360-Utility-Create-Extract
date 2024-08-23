import os
import subprocess

def extract_xiso_from_files(delete_after=False):
    print("Batch XISO Extract v1.0\n")
    print("BY: BLAHPR 2024\n")

    # Specify the ISO folder
    iso_folder = "x_ISO"
    
    print(f"READING xISO FILES: {iso_folder}' DIRECTORY...")

    # List all .iso files in the ISO folder
    iso_files = [f for f in os.listdir(iso_folder) if f.endswith('.iso')]

    for iso_file in iso_files:
        print(f"\nEXTRACTING: {iso_file}\n")

        # Run the extraction command
        iso_path = os.path.join(iso_folder, iso_file)
        result = subprocess.run(["x_tool/extract-xiso.exe", "-x", iso_path], capture_output=True)
        
        if result.returncode != 0:
            print(f"SKIPPING: \n>FOLDER EXISTS<> {iso_file}: >FOLDER EXISTS<")
        else:
            print(f"SUCCESS: \n{iso_file}")

            # Delete the ISO file if the option is selected
            if delete_after:
                print(f"\nDELETING: \n{iso_file}")
                os.remove(iso_path)

    print("\nALL DONE COMPLETE.\n")
    input("Press Enter to continue...")

if __name__ == "__main__":
    # Set delete_after flag to False by default
    extract_xiso_from_files(delete_after=False)
