# Program Objectives
- Create a web application to display jobs stored in the database and allow user to insert information about themselves to the database.

# Dependencies (reference requirements.txt for libraries)
- PostgreSQL 14, Python 3.9+, Django 5.1.6, django-formtools 2.5.1, psycopg[binary, pool] 3.2.5, python-decouple 3.8, beautifulsoup4 4.13.3 google-genai 1.5.0 xhtml2pdf 0.2.17 markdown2 2.5.3

# PostgreSQL on Ubuntu, according to Google Gemini
- Ubuntu 22.04 comes with PostgreSQL 14 by default.
- Ubuntu 24.04 comes with PostgreSSQL 15 by default.
- Should you need to reinstall PostgreSQL, run this command: apt install postgresql-14
- To start the server, run this command: sudo systemctl start postgresql

# How to Run the Project (Sprint 4 - If you did NOT complete Sprint 3)
- First, start the PostgreSQL server. This project utilizes PostgreSQL v14, therefore, if you have any newer versions,
  you will be all set. If not, please download at least v14.
- Place the .env file inside the StevenSousa_Project_1 folder.
- If your default PostgreSQL credentials are not "postgres", then make sure to update lines 11-13 in .env to your local setup. It is CRUCIAL that this project connects to your local PostgreSQL server.
- Create a .venv inside StevenSousa_Project_1/ by running the command "python3 -m venv .venv"
- Start the .venv by running the command "source .venv/bin/activate"
- Optional: upgrade pip by running the command "pip install --upgrade pip"
- Install the dependencies by running the command "pip install -r requirements.txt"
- cd into StevenSousa_Project1/ResumeBuilder and run the command "python manage.py create_db". This will connect to your local PostgreSQL server and check if DB_NAME, DB_USER exists in the server. If not, it will create them and assign DB_PASSWORD to the new user.
- Create Django managed tables inside the newly created database by running "python manage.py migrate"
- Add json jobs into Django managed table by running the command "python manage.py data_processing"
- Create a Django superuser by running the command "python manage.py createsuperuser" and follow the terminal instructions
- Start the Django server by running the command "python manage.py runserver"
- Open your browser and navigate to "http://localhost:8000" to view the web application
- To access the admin page, navigate to "http://localhost:8000/admin" and login with the superuser credentials (Highly recommended if you want a "birds-eye" view of the database)


# How to Run the Project (Sprint 4 - if you completed Sprint 3)
- First, start the PostgreSQL server. This project utilizes PostgreSQL v14, therefore, if you have any newer versions,
  you will be all set. If not, please download at least v14.
- Place the .env file inside the StevenSousa_Project_1 folder.
- If your default PostgreSQL credentials are not "postgres", then make sure to update lines 11-13 in .env to your local setup. It is CRUCIAL that this project connects to your local PostgreSQL server.
- Create a .venv inside StevenSousa_Project_1/ by running the command "python3 -m venv .venv"
- Start the .venv by running the command "source .venv/bin/activate"
- Optional: upgrade pip by running the command "pip install --upgrade pip"
- Install the dependencies by running the command "pip install -r requirements.txt"
- In Sprint 3, the database and user were created, but with sprint 4, a new app was added: gemini, therefore, cd into ResumeBuilder/ and run the following command: "python manage.py makemigrations" and then "python manage.py migrate".
- Alternatively, you can drop the "ssousa_project1" database and run the command "python manage.py create_db" to create the database and user again, and then "python manage.py migrate" to create the tables. (This is what I did on my second computer when I went to test the project from scratch)
- Start the Django server by running the command "python manage.py runserver"
- Open your browser and navigate to "http://localhost:8000" to view the web application
- Create a Django superuser by running the command "python manage.py createsuperuser" and follow the terminal instructions
- Start the Django server by running the command "python manage.py runserver"
- Open your browser and navigate to "http://localhost:8000" to view the web application
- To access the admin page, navigate to "http://localhost:8000/admin" and login with the superuser credentials (Highly recommended if you want a "birds-eye" view of the database)

# How to Run Tests
- With your .venv activated and in the directory StevenSousa_Project_1/ResumeBuilder/, run the command "python manage.py test jobs.tests candidate.tests genmini.tests"
- A total of 11 tests will run. 5 tests for the jobs app (sprint 2 & 3), 2 tests for the candidate app (sprint 3), and 4 from the gemini app (sprint 4).

# How to Create a User and Profile
- If you created a superuser, the web app will automatically log in as the superuser. Please click log out in the navbar.
- Click on the "Sign Up" button in the navbar to create a new profile.
- The sign up process is divided into 5 steps:
- Step 1: Create a user (username, email, password, first name, last name, etc) - static information
- Step 2: Create a profile
- Step 3: Add experience
- Step 4: Add projects
- Step 5: Add references
- Steps 3 - 5 are going to be information related to your profile. Once you have filled out all the information, click on the "Save" button to save your information to the database.
- You will be redirected to the home page and will already be logged in as the user you just created.
- If you want to view your profile information, click "Edit User" and you will go back to the Step 1 of creating a user, however this time the information will be filled out with the information you just entered. In step 2, you can either create a new profile or select a profile from the dropdown.

# Current bugs
- Currently there are no known bugs. If you find any, please let me know.