# Program Objectives
- Programmatically parse through the rapid_jobs2.json file (read file line by line for valid json)
- Save parsed json objects to DB (PostgreSQL)
- Send any job description from DB to Gemini

# Dependencies
- Python 3.9+, dotenv, os, re, google.generativeai, google.generativeai.types, API key for Gemini, markdown, xhtml2pdf

# How to install dependencies
- Python: https://www.python.org/downloads/
- os & re: standard python libraries, no need to pip install
- dotenv: pip install python-dotenv
- google.generativeai: pip install -q -U google-generativeai
- markdown: pip install markdown
- xhtml2pdf: pip install xhtml2pdf
- API key located in .env file