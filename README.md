# ecoinvent

To run the app:

1. Clone the repo (or download zip)

(If you have pip with virtual environment installed)

2. On the project level (with apps, requirements.txt etc...) in the terminal run "virtualenv venv"
3. run "source venv/bin/activate" to activate the virtual env

(if you don't just run a virtual env however you please here)

4. run "pip install -r requirements.txt" to install project requirements
5. run "python manage.py makemigrations"
6. run "python manage.py migrate"
7. run "python manage.py runserver" to start up the server on localhost and login (password is hashed before storing and must have uppercase, symbol, number. I use Password1!)
8. Upload ecoSpold datasets
