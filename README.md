README

Overview

This repository contains two key scripts:

Python Encryption Script (phantom.py):

Used to encrypt and decrypt files and folders using a password-based key derivation and symmetric encryption.
PowerShell Setup and Encryption Script (setup_and_encrypt.ps1):

Automates the installation of Python, the required libraries, and runs the encryption script on specified directories.
Python Encryption Script (phantom.py)

Description
The Python script phantom.py performs encryption and decryption of files and directories using the cryptography library. It uses a password-based key derivation function to generate an encryption key, which is then used to encrypt or decrypt files.

Usage
To use the phantom.py script directly, you need to pass the path of the file or folder you want to encrypt or decrypt, along with the required options.

Key Features
Generate a cryptographic key from a password and salt.
Encrypt and decrypt individual files or entire folders.
Recursively process directories to handle all contained files.
PowerShell Setup and Encryption Script (setup_and_encrypt.ps1)

Description
The PowerShell script setup_and_encrypt.ps1 automates the installation of Python and the required libraries. It then uses the phantom.py script to encrypt user data on a Windows PC.

Steps
Download and Install Python:

Downloads Python from the official source and installs it.
Install Required Libraries:

Installs the cryptography library using pip.
Encrypt User Data:

Encrypts specified directories (C:\Users\ and C:\ProgramData) to protect user files and common application data.
Usage
Save the PowerShell script as setup_and_encrypt.ps1.
Open PowerShell with administrative privileges.
Execute the script:
powershell
Copy code
.\setup_and_encrypt.ps1
Disclaimer and Legal Concerns

Disclaimer
This repository is intended for educational and testing purposes only. The scripts provided are designed to demonstrate file encryption and decryption and should not be used maliciously. Unauthorized encryption of data without proper authorization is illegal and unethical.

Legal Concerns
Authorization:

Ensure you have explicit permission before running these scripts on any system. Unauthorized use of these scripts can lead to legal consequences.
Data Loss:

The use of encryption involves risks, including the potential for data loss if the encryption keys are lost. It is essential to back up data before encryption.
Ethical Use:

Use these scripts responsibly and in compliance with all applicable laws and regulations. Misuse of these scripts can result in legal action.
No Warranty:

The scripts are provided "as is" without any warranty of any kind. The authors are not liable for any damage or loss resulting from the use of these scripts.
By using these scripts, you acknowledge that you have read, understood, and agree to the above disclaimer and legal concerns.
