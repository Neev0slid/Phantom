import pathlib
import os
import secrets
import base64
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

def generate_salt(size=16):
    """Generate the salt used for the key derivation,
    `size` is the length of the salt to generate"""
    return secrets.token_bytes(size)

def derive_key(salt, password):
    """Derive the key from the `password` using the passed `salt`"""
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())

def load_salt():
    # Load salt from salt.salt file
    return open("salt.salt", "rb").read()

def generate_key(password, salt_size=16, load_existing_salt=False, save_salt=True):
    """Generate a key from a `password` and the salt.
    If `load_existing_salt` is True, it'll load the salt from a file in the current directory called 'salt.salt'.
    If `save_salt` is True, then it will generate a new salt and save it to 'salt.salt'"""
    
    if load_existing_salt:
        # Load existing salt
        salt = load_salt()
    elif save_salt:
        # Generate new salt and save it
        salt = generate_salt(salt_size)
        with open("salt.salt", "wb") as salt_file:
            salt_file.write(salt)
    # Generate the key from the salt and the password
    derived_key = derive_key(salt, password)
    # Encode it using base64 and return it
    return base64.urlsafe_b64encode(derived_key)

def encrypt(filename, key):
    """Given a filename (str) and key (bytes), it encrypts the file and writes it"""
    f = Fernet(key)
    with open(filename, "rb") as file:
        # Read all file data
        file_data = file.read()
    # Encrypt data
    encrypted_data = f.encrypt(file_data)
    # Write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)

def decrypt(filename, key):
    """Given a filename (str) and key (bytes), it decrypts the file and writes it"""
    f = Fernet(key)
    with open(filename, "rb") as file:
        # Read the encrypted data
        encrypted_data = file.read()
    # Decrypt data
    try:
        decrypted_data = f.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        print("[!] Invalid token, most likely the password is incorrect")
        return
    # Write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)

def encrypt_folder(foldername, key):
    # If it's a folder, encrypt the entire folder (i.e., all the containing files)
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"[*] Encrypting {child}")
            encrypt(child, key)
        elif child.is_dir():
            encrypt_folder(child, key)

def decrypt_folder(foldername, key):
    # If it's a folder, decrypt the entire folder
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"[*] Decrypting {child}")
            decrypt(child, key)
        elif child.is_dir():
            decrypt_folder(child, key)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="File Encryptor script with a Password")
    parser.add_argument("path", help="Path to encrypt/decrypt, can be a file or an entire folder")
    parser.add_argument("-s", "--salt-size", help="If this is set, a new salt with the passed size is generated", type=int)
    parser.add_argument("-e", "--encrypt", action="store_true", help="Whether to encrypt the file/folder, only -e or -d can be specified.")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Whether to decrypt the file/folder, only -e or -d can be specified.")
    
    args = parser.parse_args()
    
    if args.encrypt:
        password = getpass.getpass("Enter the password for the encryption: ")
    elif args.decrypt:
        password = getpass.getpass("Enter the password you used for encryption: ")
    
    if args.salt_size:
        key = generate_key(password, salt_size=args.salt_size, save_salt=True)
    else:
        key = generate_key(password, load_existing_salt=True)
    
    encrypt_ = args.encrypt
    decrypt_ = args.decrypt
    
    if encrypt_ and decrypt_:
        raise TypeError("Please specify whether to encrypt the file or decrypt it.")
    elif encrypt_:
        if os.path.isfile(args.path):
            # If it is a file, encrypt it
            encrypt(args.path, key)
        elif os.path.isdir(args.path):
            encrypt_folder(args.path, key)
    elif decrypt_:
        if os.path.isfile(args.path):
            decrypt(args.path, key)
        elif os.path.isdir(args.path):
            decrypt_folder(args.path, key)
    else:
        raise TypeError("Please specify whether you want to encrypt the file or decrypt it.")
