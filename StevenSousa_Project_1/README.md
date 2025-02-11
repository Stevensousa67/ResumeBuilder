# Program Objectives
- Programmatically parse through the rapid_jobs2.json and rapidResults.json files
- Save parsed json objects to DB (PostgreSQL)
- Send any job description from DB alongside my information (located in .env) to Gemini

# Dependencies
- Python 3.9+, dotenv, google.generativeai, API key for Gemini, PostgreSQL 14

# How to install dependencies
- cd into StevenSousa_Project_1, run the command "source .venv/bin/activate" and then run the command "pip install -r requirements.txt"
- Download and install PostgreSQL 14 if needed
- API key and DB info located in .env file

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
- Run the main.py file

# What to Expect?

- Upon running main.py, the program will connect to your postgres server using default credentials, create a new user,
  database, and assign the new user as owner of the new database, if both user and database do not exist already.
- Program will close the existing connection to the PostgreSQL server and reconnect using the new user and database
  credentials
- Program will then parse the json files located in StevenSousa_Project_1/data and save their contents in the database
- Upon saving all jobs in the files, the program will then close.

