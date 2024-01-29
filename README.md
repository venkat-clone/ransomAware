# RansomAware
### DECRYPTING DATA INFECTED WITH MAZE RANSOMWARE
The persistence threat of ransomware has become a critical concern in cybersecurity landscapes,
needing innovative countermeasures. This project addresses this challenge through a multifaceted
approach. Primarily, a specialized decryptor has been developed to restore files encrypted by
Maze ransomware, utilizing extracted Blob Private Keys and the Chacha20/8 key from ransom
notes.
Complementing this, the project introduces a secure backup mechanism to Mega cloud with
Fernet (AES) encryption, secure data protection strategies. Additionally, a robust file scanning
feature calculates SHA256 hashes, allowing the identification of potential malware. The project
is underpinned by a meticulous methodology, encompassing data collection, decryption
processes. The implementation features a modular system architecture and RSA & chacha20/8
algorithms tailored to the of Maze ransomware.
Results indicate a high success rate in file recovery, efficient performance metrics. This abstract
encapsulates the comprehensive efforts to counter Maze ransomware, providing a versatile
solution that amalgamates decryption, secure backup, and malware detection for an enhanced
cybersecurity posture. 
### Cloning into local system
```commandline
git clone https://github.com/venkat-clone/ransomAware
cd ransomAware
```
### To run Frontend in the dev environment run the following command
#### for mac & Linux run
```commandline
pip install mega.py pycryptodome pyinstaller flet cryptography
./restart.sh
```
#### for windows run
```commandline
cd frontend
flet run __main__.py
```
### To start the server run the following commands
```commandline
cd backendApis
pip install django djangoestframework
python manage.py run
```

### To build the exigutable for any platform(Mac/Linux/Windows) run the following command
```commandline
cd frontend
pip install mega.py pycryptodome pyinstaller flet cryptography
flet pack __main__.py
```
