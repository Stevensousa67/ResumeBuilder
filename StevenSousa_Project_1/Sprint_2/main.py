"""
Author: Steven Sousa
Prof.: John Santore
Institution: Bridgewater State University - COMP490 - Senior Design & Development
Version: 06Feb2025

Description: This program builds upon the achievements of Spring_1 main.py. In this version, the program will
programmatically parse the rapid_jobs2.json and rapidResults.json files in order to save each job into a PostgreSQL DB
and provide the ability to send any job from the DB as a prompt to Google AI Studio.
"""
# Import dependencies
import os
import dotenv
import DBUtils
import Data_Processing

# Load environment variables
dotenv.load_dotenv(os.path.join(os.path.dirname(os.getcwd()), '.env'))

# Create DB Connection
conn, cursor = DBUtils.open_db(os.getenv('DB_NAME'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'),
                               os.getenv('DB_HOST'), os.getenv('DB_PORT'))
# Create DB
DBUtils.setup_db(cursor, conn)

# Process data
Data_Processing.read_json_and_save_to_excel('rapid_jobs2.json')

# Exit program
print('Program finished successfully.')

