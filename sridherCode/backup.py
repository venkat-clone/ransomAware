import os
import zipfile
from cryptography.fernet import Fernet
from mega import Mega

tmpDir = 'backup_tmp'

# Define the folder you want to encrypt
folder_to_encrypt = f"{tmpDir}"

# Generate or load the Fernet key
key_filename = f"{tmpDir}/fernet_key.key"

if not os.path.exists(tmpDir):
    os.mkdir(tmpDir)

if not os.path.exists(key_filename):
    # Generate a Fernet key if it doesn't exist
    key = Fernet.generate_key()
    with open(key_filename, 'wb') as key_file:
        key_file.write(key)
else:
    # Load the Fernet key if it exists
    with open(key_filename, 'rb') as key_file:
        key = key_file.read()

# Create a zip file to store the encrypted contents
zip_file_name = f"{tmpDir}/encrypted_folder.zip"
zipf = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)

# Initialize the Fernet cipher with the key
cipher = Fernet(key)

# Encrypt and add the files from the folder to the zip file
for root, dirs, files in os.walk(folder_to_encrypt):
    for file in files:
        file_path = os.path.join(root, file)
        with open(file_path, 'rb') as file_to_encrypt:
            plaintext = file_to_encrypt.read()

        # Encrypt the file using Fernet
        encrypted_data = cipher.encrypt(plaintext)

        # Store the encrypted data in the zip file with the same directory structure
        zip_file_path = os.path.relpath(file_path, folder_to_encrypt)
        zipf.writestr(zip_file_path, encrypted_data)

zipf.close()

print(f"Files encrypted and saved to '{zip_file_name}'")

# Authenticate and upload the encrypted zip file to Mega
mega = Mega()
m = mega.login("mailuser0102@gmail.com", "20U51A6207")  # Replace with your Mega email and password

# Upload the encrypted zip file to Mega
m.upload(zip_file_name)

print(f"File '{zip_file_name}' uploaded to Mega")

# Clean up - remove the temporary encrypted zip file
os.remove(zip_file_name)

# Save the Fernet key to a secure location for later decryption
# You can save it to a secure USB drive, a password manager, or another secure location
secure_key_filename = f"{tmpDir}/fernet_key.key"

with open(secure_key_filename, 'wb') as secure_key_file:
    secure_key_file.write(key)

print("Fernet key saved to a secure location.")
