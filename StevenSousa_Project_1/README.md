# Program Objectives
- Programmatically parse through the rapid_jobs2.json and rapidResults.json files
- Save parsed json objects to Google Cloud Provider PostgreSQL 14 database.
- If you want to use a local DB, simply change the GCP_DB_HOST variable in .env to "localhost" and follow the instructions below.

# Dependencies (reference requirements.txt for libraries)
- PostgreSQL 14, Python 3.9+, dotenv, psycopg, pytest, pytest-mock

# PostgreSQL on Ubuntu, according to Google Gemini
- Ubuntu 22.04 comes with PostgreSQL 14 by default.
- Ubuntu 24.04 comes with PostgreSSQL 15 by default.
- Should you need to reinstall PostgreSQL, run this command: apt install postgresql-14
- To start the server, run this command: sudo systemctl start postgresql

# How to Run
- First, start the PostgreSQL server. This project utilizes PostgreSQL v14, therefore if you have any newer versions,
  you will be all set. If not, please download at least v14.
- Place the .env file inside the StevenSousa_Project_1 folder.
- Create a .venv inside StevenSousa_Project_1
- Open your terminal, navigate to the StevenSousa_Project_1 folder and start the .venv by running the command "source
  .venv/bin/activate"
- Still in your terminal, install the dependencies by running the command "pip install -r requirements.txt"
- Run project by typing the command: "python3 -m src.main"
- Run tests by typing the command: "python3 -m pytest tests/"
- Should you have PORT issues (PORT being used), simply change the PORT value for the variable DB_PORT inside of .env until you find an available port.

# What to Expect?
- Upon running main.py, the program will connect to your postgres server using default credentials, create a new user,
  database, and assign the new user as owner of the new database, if both user and database do not exist already.
- Program will close the existing connection to the PostgreSQL server and reconnect using the new user and database
  credentials
- Program will then parse the json files located in StevenSousa_Project_1/data and save their contents in the database
- Upon saving all jobs in the files, the program will then close.

# Sprint 3
- First, start the PostgreSQL server. This project utilizes PostgreSQL v14, therefore if you have any newer versions,
  you will be all set. If not, please download at least v14.
- Place the .env file inside the StevenSousa_Project_1 folder.
- If your default PostgreSQL credentials are not "postgres", then make sure to update lines 11-13 in .env to your local setup. It is CRUCIAL that this project connects to your local PostgreSQL server.
- Create a .venv inside StevenSousa_Project_1/
- In your terminal, navigate to the StevenSousa_Project_1 folder and start the .venv by running the command "source
  .venv/bin/activate"
- Still in your terminal but now with the .venv activated, install the dependencies by running the command "pip install -r requirements.txt"
- cd into ResumeBuilder/ and run the command "python manage.py ensure_db". This will connect to your local PostgreSQL server and check if DB_NAME, DB_USER exists in the server. If not, it will create them and assign DB_PASSWORD to the new user.
- Create Django managed tables by running "python manage.py migrate"
- Add json jobs into Django managed table by running the command "python manage.py Data_Processing"
- Create a Django superuser by running the command "python manage.py createsuperuser" and follow the terminal instructions
- Start the Django server by running the command "python manage.py runserver"