import os
import subprocess
import sys

def run_script(script_name):
    script_path = os.path.join(os.path.dirname(__file__), 'scripts', script_name)
    if os.path.exists(script_path):
        try:
            subprocess.run([sys.executable, script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the script: {e}")
    else:
        print(f"Script {script_name} does not exist.")

def display_dwbuilder_design():
    design = """
    *********************************************
    *                                           *
    *               DWBuilder                   *
    *                                           *
    *********************************************
    """
    print(design)

def main():
    display_dwbuilder_design()
    
    scripts = {
        '1': 'dwbuilder.py',
        '2': 'dbuilder.py',
        '3': 'hibuilder.py',
        '4': 'slab.py',
        '5': 'polarization.py',
        '6': 'supercell.py',
        '7': 'vasp2cif.py'
    }

    print("Select a script to run:")
    for key, value in scripts.items():
        print(f"{key}: {value}")

    choice = input("Enter the number of the script to run: ").strip()

    if choice in scripts:
        run_script(scripts[choice])
    else:
        print("Invalid choice. Please select a valid script number.")

if __name__ == "__main__":
    main()
