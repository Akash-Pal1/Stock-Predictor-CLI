import subprocess

def check_library_installed(library_name):
    result = subprocess.run(['pip', 'show', library_name], capture_output=True, text=True)
    return result.returncode == 0

def install_libraries(library_names):
    to_install = [library for library in library_names if not check_library_installed(library)]
    if to_install:
        try:
            subprocess.check_call(['pip', 'install'] + to_install)
            print("Libraries installed successfully.")
        except subprocess.CalledProcessError:
            print("Failed to install libraries. Please make sure you have pip installed.")
    else:
        print()

def run_main_script():
    try:
        subprocess.check_call(['python', 'stockMain.py'])
    except subprocess.CalledProcessError:
        print("Failed to run the main script.")

if __name__ == "__main__":
    required_libraries = ['pip', 'install', 'pandas', 'sklearn','argparse','yfinance','stocksymbol']
    install_libraries(required_libraries)
    run_main_script()

