# info.py
import os

def display_info():
    print("Welcome to My Library!")
    print("Available Modules and Files:")
    print("Welcome to My Crypto Library!")
    print("This library supports the following ciphers:")
    print("1. Caesar Cipher")
    print("2. Playfair Cipher")
    print("3. Hill Cipher")
    print("4. Vigenère Cipher")
    print("5. rsa ")
    print("6. dss ")
    print("7. md5 ")
    print("8. aes ")
    print("9. des ")
    print("10. ids ")
    print("11. rail fence ")
    print("12. deffie ")
    print("13. sha12 ")
    print("\nEach cipher module includes functions for encryption and decryption.")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py"):
                print(f"- {os.path.relpath(os.path.join(root, file), base_dir)}")

    print("\nFor detailed documentation, refer to the README.md or official documentation site.")

# Alternatively, you can make this an interactive help tool by adding more specific help text for each module or file.
