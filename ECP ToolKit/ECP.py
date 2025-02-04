import os
import json
import sys
import time
import subprocess
import zipfile
from colorama import Fore, Style

# Function to install missing packages
def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError:
        print(Fore.RED + f"Failed to install {package}" + Style.RESET_ALL)

# Check and install required modules
try:
    from colorama import Fore, Style
except ImportError:
    print("Installing colorama...")
    install_package("colorama")
    from colorama import Fore, Style

# Define the path for translations and used language file
data_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Data")
languages_file = os.path.join(data_folder, "languages.json")
used_language_file = os.path.join(data_folder, "selected_language.json")

# Create Data folder if it doesn't exist
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Load the language setting from selected_language.json
def load_language():
    if os.path.exists(used_language_file):
        with open(used_language_file, "r", encoding='utf-8') as f:
            data = json.load(f)
            return data.get("selected_language", "en")
    return "en"  # Default language is English

# Set or change the language
def set_language(language):
    with open(used_language_file, "w", encoding='utf-8') as f:
        json.dump({"selected_language": language}, f)

# Function to choose language if no valid language is found
def choose_language():
    print(Fore.MAGENTA + "Choose a language:" + Style.RESET_ALL)
    print(Fore.GREEN + "1. English" + Style.RESET_ALL)
    print(Fore.GREEN + "2. Spanish" + Style.RESET_ALL)
    print(Fore.GREEN + "3. Chinese (Simplified)" + Style.RESET_ALL)
    choice = input("Enter choice (1-3): ")
    lang_map = {"1": "en", "2": "es", "3": "zh"}
    selected_lang = lang_map.get(choice, "en")

    # Set and save selected language
    set_language(selected_lang)
    print(Fore.MAGENTA + "Language set. Restart the program." + Style.RESET_ALL)
    sys.exit()

# Check if the languages file exists
if not os.path.exists(languages_file):
    print(Fore.RED + "Languages file not found!" + Style.RESET_ALL)
    sys.exit()

# Load the translations from the file
with open(languages_file, "r", encoding='utf-8') as f:
    translations = json.load(f)

# Load the language from the selected_language file
current_language = load_language()

# Check if the selected language exists in the translations file
if current_language not in translations:
    print(Fore.RED + "Language not found! Please re-download the tool." + Style.RESET_ALL)
    choose_language()

# Retrieve the messages for the selected language
messages = translations.get(current_language, translations["en"])

# Function to extract RSB files from IPA
def extract_rsb_files_from_ipa(ipa_path, output_folder):
    try:
        if not os.path.exists(ipa_path):
            print(Fore.RED + messages["ipa_missing"] + Style.RESET_ALL)
            return

        print(Fore.CYAN + messages["extracting"] + Style.RESET_ALL)
        start_time = time.time()

        with zipfile.ZipFile(ipa_path, 'r') as ipa:
            rsb_files = [f for f in ipa.namelist() if f.endswith('.rsb')]
            total_files = len(rsb_files)

            if total_files == 0:
                print(Fore.RED + messages["not_recognized"] + Style.RESET_ALL)
                return

            # Create a new folder for extracted RSB files
            rsb_folder = os.path.join(output_folder, "RSB_Files")
            if not os.path.exists(rsb_folder):
                os.makedirs(rsb_folder)

            extracted_count = 0
            extracted_file_names = []

            for i, file in enumerate(rsb_files):
                extracted_path = os.path.join(rsb_folder, os.path.basename(file))
                with ipa.open(file) as src, open(extracted_path, 'wb') as dest:
                    dest.write(src.read())
                extracted_count += 1
                extracted_file_names.append(os.path.basename(file))

                progress = (i + 1) / total_files * 100
                elapsed_time = time.time() - start_time
                print(f"{messages['progress']}: {progress:.2f}% | {messages['time_elapsed']}: {elapsed_time:.2f}s")

            print(Fore.GREEN + messages["done"] + Style.RESET_ALL)
            print(f"{messages['total_extracted']} {extracted_count}")
            print(messages["extracted_files"], ", ".join(extracted_file_names))

    except Exception as e:
        print(Fore.RED + messages["error"] + ": " + str(e) + Style.RESET_ALL)

# Main logic
print(Fore.MAGENTA + f"{messages['welcome']}\n{messages['version']}\n{messages['youtube']}\nMade By LuvTime" + Style.RESET_ALL)

ipa_path = input(Fore.CYAN + messages["enter_ipa_path"] + Style.RESET_ALL).strip('"')

# Allow absolute paths across different drives
ipa_path = os.path.abspath(ipa_path)
ipa_folder = os.path.dirname(ipa_path)
output_folder = ipa_folder

# Extract RSB files from the IPA
extract_rsb_files_from_ipa(ipa_path, output_folder)

# Wait for user input before exiting
input(Fore.CYAN + messages['press_enter'] + Style.RESET_ALL)
