#!/usr/bin/env python3
import os
import sys
from cryptography.fernet import Fernet
from colorama import init, Fore, Style

# Initialize Colorama
init()

def load_key(file_path):
    return open(file_path, "rb").read()

def decrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        file_data = file.read()

    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(file_data)

    with open(file_path, "wb") as file:
        file.write(decrypted_data)

def decrypt_directory(directory_path, key, recursive=False):
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key)
        if not recursive:
            break

def main():
    print(Fore.CYAN + "Select an option:" + Style.RESET_ALL)
    print("1 Decrypt a single file")
    print("2 Decrypt all files in a directory")
    print("3 Decrypt all files in a directory and its subdirectories")
    
    choice = input(Fore.GREEN + "Enter your choice: " + Style.RESET_ALL)

    if choice not in ['1', '2', '3']:
        print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
        sys.exit(1)

    path = input(Fore.GREEN + "Enter the path: " + Style.RESET_ALL)

    if not os.path.exists(path):
        print(Fore.RED + f"Error: The path {path} does not exist." + Style.RESET_ALL)
        sys.exit(1)

    print()
    print(Fore.CYAN + "Select a key option:" + Style.RESET_ALL)
    print("1. Use a key file")
    print("2. Enter the key manually")
    
    key_choice = input(Fore.GREEN + "Enter your choice (1/2): " + Style.RESET_ALL)

    if key_choice == '1':
        key_path = input(Fore.GREEN + "Enter the path to the key file: " + Style.RESET_ALL)
        if not os.path.isfile(key_path):
            print(Fore.RED + f"Error: The key file {key_path} does not exist." + Style.RESET_ALL)
            sys.exit(1)
        key = load_key(key_path)
        print(Fore.GREEN + f"Key loaded from {key_path}: {key.decode()}" + Style.RESET_ALL)
    elif key_choice == '2':
        key_input = input(Fore.GREEN + "Enter the key (base64 encoded): " + Style.RESET_ALL).strip()
        try:
            key = key_input.encode()
            Fernet(key)  # Validate the key format
            print(Fore.GREEN + f"Key entered: {key.decode()}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error: Invalid key format. {e}" + Style.RESET_ALL)
            sys.exit(1)
    else:
        print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
        sys.exit(1)

    if choice == '1':
        if os.path.isfile(path):
            decrypt_file(path, key)
        else:
            print(Fore.RED + f"Error: The path {path} is not a file." + Style.RESET_ALL)
    elif choice == '2':
        if os.path.isdir(path):
            decrypt_directory(path, key, recursive=False)
        else:
            print(Fore.RED + f"Error: The path {path} is not a directory." + Style.RESET_ALL)
    elif choice == '3':
        if os.path.isdir(path):
            decrypt_directory(path, key, recursive=True)
        else:
            print(Fore.RED + f"Error: The path {path} is not a directory." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Error: Invalid choice." + Style.RESET_ALL)

    print(Fore.LIGHTGREEN_EX + "Decryption completed successfully." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
