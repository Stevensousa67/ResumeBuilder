"""
Author: Steven Sousa
Prof.: John Santore
Institution: Bridgewater State University - COMP490 - Senior Design & Development
Version: 06Feb2025

This file will parse the json files containing jobs and save them to the DB created in main.py
"""
# Import dependencies
import json
import DBUtils


def process_json(filename: str, conn: DBUtils.Connection, cursor: DBUtils.Cursor) -> None:
    """
    Parses job data from JSON files and saves it to the database.
    Handles both array-of-objects and object-per-line JSON formats.

    :param filename: JSON file containing jobs.
    :param conn: Database connection.
    :param cursor: Database cursor.
    :return: None
    """

    with open(filename) as file:
        for line in file:
            try:
                data = json.loads(line.strip())

                # Handle both JSON formats:
                if isinstance(data, list):  # Array of objects
                    objects = data
                elif isinstance(data, dict):  # Single object
                    objects = [data]
                else:
                    print(f"Skipping invalid line: {line.strip()}")
                    continue  # Skip lines with invalid JSON structure


                for obj in objects:
                    job_id = obj.get('id', 'N/A')
                    job_title = obj.get('title', 'N/A')
                    company_name = obj.get('company', 'N/A')
                    job_description = obj.get('description', 'N/A')
                    location = obj.get('location', 'N/A')

                    # Handle different salary keys depending on file passed in:
                    min_salary = convert_salary(obj.get('min_salary', obj.get('min_amount', "")))
                    max_salary = convert_salary(obj.get('max_salary', obj.get('max_amount', "")))
                    salary_time = obj.get('salary_time', obj.get('interval', 'yearly'))

                    posted_date = obj.get('datePosted', obj.get('date_posted', 'N/A'))

                    # Handle different URL and remote keys:
                    url = 'URL Not Found'
                    if 'jobProviders' in obj:
                        job_providers = obj.get('jobProviders', [])
                        url = job_providers[0].get('url', 'URL Not Found') if job_providers else 'URL Not Found'
                    elif 'job_url_direct' in obj:
                        url = obj.get('job_url_direct', 'URL Not Found')

                    remote = False
                    if 'remote' in str(location).lower():
                       remote = True
                    elif 'is_remote' in obj:
                        remote = obj.get('is_remote', False)
                        if remote == '':
                            remote = False

                    job_tuple = (job_id, job_title, company_name, job_description, location, min_salary, max_salary,
                                 salary_time, posted_date, url, remote)
                    DBUtils.insert_job(cursor, conn, job_tuple)

            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)


def convert_salary(salary: str) -> int:
    """Converts a salary string to an integer, handling empty strings, None, and non-numeric values.
    :param salary: Salary to be converted.
    :return: Converted salary.
    """

    if not (salary and salary.isnumeric()):
        return 0
    try:
        return int(float(salary))  # Convert to float first to handle decimals
    except ValueError:
        print(f"Unexpected salary format: {salary}")
        return 0
