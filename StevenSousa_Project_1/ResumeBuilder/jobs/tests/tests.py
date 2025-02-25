from django.test import TestCase
from django.core.management import call_command
from django.conf import settings
import psycopg
import sys
import io


class TestJobDatabase(TestCase):
    def setUp(self):
        # Redirect sys.stdout to capture command output (optional, only if needed)
        self.stdout = io.StringIO()
        sys.stdout = self.stdout

        # No manual database creation needed; Django handles it

    def test_01_database_connection(self):
        # Verify connection to the test database
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
                    self.assertTrue(True, f"Connection to '{settings.DATABASES['default']['NAME']}' successful!")
        except psycopg.OperationalError as e:
            self.fail(f"Error connecting to test database '{settings.DATABASES['default']['NAME']}': {e}")

    def test_02_table_exists(self):
        # Verify the table was created by Django's migrations
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
                    table_name = 'test_django_jobs'
                    cursor.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}');")
                    exists = cursor.fetchone()[0]
                    self.assertTrue(exists, f"Table '{table_name}' exists in test database!")
        except psycopg.OperationalError as e:
            self.fail(f"Error querying test database: {e}")

    # def test_03_save_data(self):
    #     # Call the command to save data
    #     call_command('data_processing')
    #
    #     # Verify data was saved
    #     try:
    #         with psycopg.connect(
    #             dbname=settings.DATABASES['default']['NAME'],
    #             user=settings.DATABASES['default']['USER'],
    #             password=settings.DATABASES['default']['PASSWORD'],
    #             host=settings.DATABASES['default']['HOST'],
    #             port=settings.DATABASES['default']['PORT'],
    #             autocommit=True
    #         ) as conn:
    #             with conn.cursor() as cursor:
    #                 table_name = 'test_django_jobs'
    #                 cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    #                 count = cursor.fetchone()[0]
    #                 self.assertGreater(count, 0, "Data saved to the jobs table successfully!")
    #     except psycopg.OperationalError as e:
    #         self.fail(f"Error querying test database: {e}")

    def tearDown(self):
        # Reset sys.stdout
        sys.stdout = sys.__stdout__