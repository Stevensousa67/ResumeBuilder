from django.test import TransactionTestCase
from django.conf import settings
from django.core.management import call_command
from django.urls import reverse
import psycopg
import sys
import io
import os
import json


class TestJobDatabase(TransactionTestCase):
    def setUp(self):
        self.stdout = io.StringIO()
        sys.stdout = self.stdout

        call_command('data_processing')

    def test_01_database_connection(self):
        try:
            with psycopg.connect(
                    dbname=settings.DATABASES['default']['NAME'],
                    user=settings.DATABASES['default']['USER'],
                    password=settings.DATABASES['default']['PASSWORD'],
                    host=settings.DATABASES['default']['HOST'],
                    port=settings.DATABASES['default']['PORT'],
                    autocommit=True
            ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1;")
                    self.assertTrue(True,
                                    f"Connection to '{settings.DATABASES['default']['NAME']}' successful!")
        except psycopg.OperationalError as e:
            self.fail(f"Error connecting to test database '{settings.DATABASES['default']['NAME']}': {e}")

    def test_02_table_exists(self):
        try:
            with psycopg.connect(
                    dbname=settings.DATABASES['default']['NAME'],
                    user=settings.DATABASES['default']['USER'],
                    password=settings.DATABASES['default']['PASSWORD'],
                    host=settings.DATABASES['default']['HOST'],
                    port=settings.DATABASES['default']['PORT'],
                    autocommit=True
            ) as conn:
                with conn.cursor() as cursor:
                    table_name = 'django_jobs'
                    cursor.execute(
                        f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}');")
                    exists = cursor.fetchone()[0]
                    self.assertTrue(exists, f"Table '{table_name}' exists in test database!")
        except psycopg.OperationalError as e:
            self.fail(f"Error querying test database: {e}")

    def test_03_save_data(self):
        try:
            with psycopg.connect(
                    dbname=settings.DATABASES['default']['NAME'],
                    user=settings.DATABASES['default']['USER'],
                    password=settings.DATABASES['default']['PASSWORD'],
                    host=settings.DATABASES['default']['HOST'],
                    port=settings.DATABASES['default']['PORT'],
                    autocommit=True
            ) as conn:
                with conn.cursor() as cursor:
                    table_name = 'django_jobs'
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                    count = cursor.fetchone()[0]
                    self.assertEqual(count, 2035, "Data saved to the jobs table successfully!")
        except psycopg.OperationalError as e:
            self.fail(f"Error querying test database: {e}")

    def test_04_fetch_specific_job(self):
        base_path = settings.BASE_DIR
        json_file_path = os.path.join(base_path, 'ResumeBuilder', 'jobs', 'tests', 'data', 'expected_results.json')

        try:
            with open(json_file_path, 'r') as file:
                content = file.read().strip()
                expected_jobs = json.loads(content)

                for index, expected_job_values in enumerate(expected_jobs, 1):
                    expected_job = {
                        'job_id': expected_job_values[0],
                        'job_title': expected_job_values[1],
                        'company_name': expected_job_values[2],
                        'job_description': expected_job_values[3],
                        'location': expected_job_values[4],
                        'min_salary': expected_job_values[5],
                        'max_salary': expected_job_values[6],
                        'salary_time': expected_job_values[7],
                        'posted_date': expected_job_values[8],
                        'url': expected_job_values[9],
                        'remote': bool(expected_job_values[10])
                    }
                    job_id = expected_job['job_id']

                    with psycopg.connect(
                            dbname=settings.DATABASES['default']['NAME'],
                            user=settings.DATABASES['default']['USER'],
                            password=settings.DATABASES['default']['PASSWORD'],
                            host=settings.DATABASES['default']['HOST'],
                            port=settings.DATABASES['default']['PORT'],
                            autocommit=True
                    ) as conn:
                        with conn.cursor() as cursor:
                            cursor.execute(
                                "SELECT job_id, job_title, company_name, job_description, location, min_salary, "
                                "max_salary, salary_time, posted_date, url, remote FROM django_jobs WHERE job_id = %s;",
                                (job_id,))
                            db_job = cursor.fetchone()

                            if db_job is None:
                                self.fail(f"No job found in database with job_id: {job_id} at index {index}")

                            db_job_dict = {
                                'job_id': db_job[0],
                                'job_title': db_job[1],
                                'company_name': db_job[2],
                                'job_description': db_job[3],
                                'location': db_job[4],
                                'min_salary': db_job[5],
                                'max_salary': db_job[6],
                                'salary_time': db_job[7],
                                'posted_date': db_job[8],
                                'url': db_job[9],
                                'remote': bool(db_job[10])
                            }

                            self.assertEqual(expected_job, db_job_dict,
                                             f"Job data mismatch for job_id: {job_id} at index {index}")

        except FileNotFoundError:
            self.fail(f"Expected results file not found at: {json_file_path}")
        except json.JSONDecodeError as e:
            self.fail(f"Invalid JSON in expected_results.json: {e}")
        except Exception as e:
            self.fail(f"Unexpected error in test_04_fetch_specific_job: {e}")

    def test_05_job_detail_display(self):
        try:
            with psycopg.connect(
                    dbname=settings.DATABASES['default']['NAME'],
                    user=settings.DATABASES['default']['USER'],
                    password=settings.DATABASES['default']['PASSWORD'],
                    host=settings.DATABASES['default']['HOST'],
                    port=settings.DATABASES['default']['PORT'],
                    autocommit=True
            ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT job_id FROM django_jobs ORDER BY RANDOM() LIMIT 1;")
                    job_id = cursor.fetchone()[0]
                    if not job_id:
                        self.fail("No job found in database to test job detail display")

            client = self.client
            url = reverse('jobs:job_details', kwargs={'job_id': job_id})
            response = client.get(url)

            self.assertEqual(response.status_code, 200, f"Failed to retrieve job details for job_id: {job_id}")
            self.assertTemplateUsed(response, 'jobs/job_details.html', "Incorrect template used for job details")

            # Get job from database for comparison
            with psycopg.connect(
                    dbname=settings.DATABASES['default']['NAME'],
                    user=settings.DATABASES['default']['USER'],
                    password=settings.DATABASES['default']['PASSWORD'],
                    host=settings.DATABASES['default']['HOST'],
                    port=settings.DATABASES['default']['PORT'],
                    autocommit=True
            ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM django_jobs WHERE job_id = %s;", (job_id,))
                    db_job = cursor.fetchone()

                    if db_job is None:
                        self.fail(f"No job found in database with job_id: {job_id}")

                    db_job_dict = {
                        'job_id': db_job[0],
                        'job_title': db_job[1],
                        'company_name': db_job[2],
                        'job_description': db_job[3],
                        'location': db_job[4],
                        'min_salary': db_job[5],
                        'max_salary': db_job[6],
                        'salary_time': db_job[7],
                        'posted_date': db_job[8],
                        'url': db_job[9],
                        'remote': bool(db_job[10])
                    }
                    if response.context:
                        job_from_response = response.context['job']

                        self.assertEqual(job_from_response.job_id, db_job_dict['job_id'], "Job ID mismatch")
                        self.assertEqual(job_from_response.job_title, db_job_dict['job_title'], "Job Title mismatch")
                        self.assertEqual(job_from_response.company_name, db_job_dict['company_name'],
                                         "Company Name mismatch")
                        self.assertEqual(job_from_response.job_description, db_job_dict['job_description'],
                                         "Job Description mismatch")
                        self.assertEqual(job_from_response.location, db_job_dict['location'], "Location mismatch")
                        self.assertEqual(job_from_response.min_salary, db_job_dict['min_salary'], "Min Salary mismatch")
                        self.assertEqual(job_from_response.max_salary, db_job_dict['max_salary'], "Max Salary mismatch")
                        self.assertEqual(job_from_response.salary_time, db_job_dict['salary_time'],
                                         "Salary Time mismatch")
                        self.assertEqual(job_from_response.posted_date, db_job_dict['posted_date'],
                                         "Posted Date mismatch")
                        self.assertEqual(job_from_response.url, db_job_dict['url'], "URL mismatch")
                        self.assertEqual(job_from_response.remote, db_job_dict['remote'], "Remote mismatch")
                    else:
                        response_content = response.content.decode('utf-8')
                        for field, value in db_job_dict.items():
                            self.assertIn(str(value), response_content,
                                          f"Field '{field}' not found in response content")

        except psycopg.OperationalError as e:
            self.fail(f"Error querying test database: {e}")
        except Exception as e:
            self.fail(f"Unexpected error in test_05_job_detail_display: {e}")


def tearDown(self):
    # Reset sys.stdout
    sys.stdout = sys.__stdout__
