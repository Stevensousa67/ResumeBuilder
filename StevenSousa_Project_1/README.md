# Program Objectives
- Programmatically parse through the rapid_jobs2.json and rapidResults.json files (read file line by line for valid json)
- Save parsed json objects to DB (PostgreSQL)
- Send any job description from DB to Gemini

# Dependencies
- Python 3.9+, dotenv, google.generativeai, API key for Gemini, PostgreSQL 17

# How to install dependencies
- cd into StevenSousa_Project_1, run the command "source .venv/bin/activate" and then run the command "pip install -r requirements.txt"
- Download and install PostgreSQL 17 (https://postgresapp.com/downloads.html) and start the server
- API key and DB info located in .env file