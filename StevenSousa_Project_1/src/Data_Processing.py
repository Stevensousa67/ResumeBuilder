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
                    min_salary = convert_salary(obj.get('salaryRange', obj.get('min_salary', '0')))
                    max_salary = convert_salary(obj.get('salaryRange', obj.get('max_salary', '0')))
                    salary_time = get_salary_frequency(obj)

                    posted_date = obj.get('datePosted', obj.get('date_posted', 'N/A'))
                    url = get_url(obj)
                    remote = get_remote_status(obj)

                    job_tuple = (job_id, job_title, company_name, job_description, location, min_salary, max_salary,
                                 salary_time, posted_date, url, remote)
                    DBUtils.insert_job(conn, cursor, job_tuple)

            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)


def get_salary_frequency(job_obj: dict) -> str:
    """
    This function returns the salary frequency for a given job object. Default return is 'yearly'.
    :param job_obj:
    :return: salary_frequency
    """

    if 'salaryRange' in job_obj:
        if 'hour' in job_obj['salaryRange']:
            return 'hourly'
        elif 'year' in job_obj['salaryRange'] or job_obj['salaryRange'] == '':
            return 'yearly'
    elif 'interval' in job_obj:
        return 'yearly' if job_obj['interval'] == '' else job_obj['interval']
    return 'yearly'


def convert_salary(salary: str) -> int:
    """Converts a salary string to an integer, handling empty strings, None, and non-numeric values.
    :param salary: Salary to be converted.
    :return: Converted salary.
    """

    if salary != '':
        return int(float(salary))
    else:
        return 0


def get_url(job_obj: dict):
    """Extracts the URL from a job object, handling different key names.
    :param job_obj: Job object.
    :return: URL.
    """

    if 'jobProviders' in job_obj:
        job_providers = job_obj.get('jobProviders', [])
        return job_providers[0].get('url', 'URL Not Found') if job_providers else 'URL Not Found'
    elif 'job_url' in job_obj:
        return job_obj.get('job_url', 'URL Not Found')
    return 'URL Not Found'


def get_remote_status(job_obj: dict):
    """Determines the remote status from a job object.
    :param job_obj: Job object.
    :return: Remote status.
    """

    if 'is_remote' in job_obj:
        return False if job_obj['is_remote'] == '' else job_obj['is_remote']
    elif 'location' in job_obj:
        return True if 'remote' in job_obj['location'].lower() or 'remote' in job_obj['title'] else False
    return False
