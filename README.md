# RansomAware

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
