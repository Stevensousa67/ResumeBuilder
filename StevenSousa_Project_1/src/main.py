"""
Author: Steven Sousa
Prof.: John Santore
Institution: Bridgewater State University - COMP490 - Senior Design & Development
Version: 06Feb2025

Description: In this version, the program will programmatically parse the rapid_jobs2.json or rapidResults.json files
in order to save each job into a PostgreSQL DB.
"""
# Import dependencies
import os

import dotenv

import DBUtils
import Data_Processing


def main():

    # Load environment variables
    dotenv.load_dotenv(os.path.join(os.path.dirname(os.getcwd()), '.env'))

    # Connect using PostgresSQL default values
    conn_default, cursor_default = DBUtils.open_db(os.getenv('DB_NAME_DEFAULT'), os.getenv('DB_USER_DEFAULT'),
                                           os.getenv('DB_PASSWORD_DEFAULT'), os.getenv('DB_HOST'),
                                                   os.getenv('DB_PORT'), autocommit=True)

    # Create custom user
    DBUtils.create_user(cursor_default, os.getenv('DB_USER'), os.getenv('DB_PASSWORD'))

    # Create custom database
    DBUtils.create_db(cursor_default, os.getenv('DB_NAME'))

    # Assign newly created database to new user
    DBUtils.assign_ownership(cursor_default, os.getenv('DB_NAME'), os.getenv('DB_USER'))

    # Close existing connection in order to change databases
    DBUtils.close_db(conn_default, cursor_default)

    # Start new database connection using new
    conn, cursor = DBUtils.open_db(os.getenv('DB_NAME'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'),
                                   os.getenv('DB_HOST'), os.getenv('DB_PORT'), autocommit=False)
    # Create table in DB
    DBUtils.setup_table(conn, cursor)

    # Process data
    Data_Processing.process_json('../data/rapidResults.json', conn, cursor)

    # # Drop table
    # DBUtils.drop_table(conn, cursor)

    # Exit program
    print('Program finished successfully.')


if __name__ == '__main__':
    main()
