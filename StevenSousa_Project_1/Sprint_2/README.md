# Program Objectives
- Programmatically parse through the rapid_jobs2.json file (read file line by line for valid json)
- Save parsed json objects to DB (PostgreSQL)
- Send any job description from DB to Gemini

# Dependencies
- Python 3.9+, dotenv, os, re, google.generativeai, google.generativeai.types, API key for Gemini, markdown, xhtml2pdf, openpyxl PostgreSQL 17

# How to install dependencies
- cd into StevenSousa_Project_1 and run the command pip install -r requirements.txt
- Download and install PostgreSQL 17 (https://postgresapp.com/downloads.html) and start the server
- API key and DB info located in .env file