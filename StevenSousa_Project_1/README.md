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