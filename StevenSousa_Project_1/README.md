# Program Objectives
- Create a web application to display jobs stored in the database and allow user to insert information about themselves to the database.

# Dependencies (reference requirements.txt for libraries)
- PostgreSQL 14, Python 3.9+, Django 5.1.6, django-formtools 2.5.1, psycopg[binary, pool] 3.2.5, python-decouple 3.8, beautifulsoup4 4.13.3 

# PostgreSQL on Ubuntu, according to Google Gemini
- Ubuntu 22.04 comes with PostgreSQL 14 by default.
- Ubuntu 24.04 comes with PostgreSSQL 15 by default.
- Should you need to reinstall PostgreSQL, run this command: apt install postgresql-14
- To start the server, run this command: sudo systemctl start postgresql

# Disclaimer regarding Sprint 1 & 2
- Because I decided to learn Django to build the web app, I was able to completely restructure my project.
- The code, including tests, pertaining to Sprint 1 & 2 were adapted for Django and became part of the "jobs" app.
- The "candidate" app was created to handle the user's profile information.

# How to Run
- First, start the PostgreSQL server. This project utilizes PostgreSQL v14, therefore, if you have any newer versions,
  you will be all set. If not, please download at least v14.
- Place the .env file inside the StevenSousa_Project_1 folder.
- If your default PostgreSQL credentials are not "postgres", then make sure to update lines 11-13 in .env to your local setup. It is CRUCIAL that this project connects to your local PostgreSQL server.
- Create a .venv inside StevenSousa_Project_1/ by running the command "python3 -m venv .venv"
- Start the .venv by running the command "source .venv/bin/activate"
- Optional: upgrade pip by running the command "pip install --upgrade pip"
- Install the dependencies by running the command "pip install -r requirements.txt"
- cd into ResumeBuilder/ and run the command "python manage.py create_db". This will connect to your local PostgreSQL server and check if DB_NAME, DB_USER exists in the server. If not, it will create them and assign DB_PASSWORD to the new user.
- Create Django managed tables inside the newly created database by running "python manage.py migrate"
- Add json jobs into Django managed table by running the command "python manage.py data_processing"
- Create a Django superuser by running the command "python manage.py createsuperuser" and follow the terminal instructions
- Start the Django server by running the command "python manage.py runserver"
- Open your browser and navigate to "http://localhost:8000" to view the web application
- To access the admin page, navigate to "http://localhost:8000/admin" and login with the superuser credentials (Highly recommended if you want a "birds-eye" view of the database)

# How to Run Tests
- With your .venv activated and in the directory StevenSousa_Proejct_1/ResumeBuilder/, run the command "python manage.py test jobs.tests candidate.tests"
- A total of 7 tests will run. 5 tests for the jobs app (sprint 2 & 3) and 2 tests for the candidate app (sprint 3).

# How to Create Profile
- If you created a superuser, the web app will automatically log in as the superuser. Please click log out in the navbar.
- Click on the "Sign Up" button in the navbar to create a new profile.
- You will first create a user (for authentication purposes) and then fill out the information related to your user (Candidate info, Experience, Projects, References)
- Once you have filled out all the information, click on the "Submit" button to save your information to the database.
- You will be redirected to the home page and will already be logged in as the user you just created.
- If you want to view your profile information, visit the /admin page (log in with your superuser credentials)

# Current bugs (2 known issues, however they are outside of Sprint 3's scope)
- Web app automatically logging you in as the superuser if such was created. 
- Once a profile is created, editing the user will bring the 4 steps of creating a user again, although this time the fields are filled out with the user's information. The issue is that the user cannot advance past Step 2 - Experience.  
