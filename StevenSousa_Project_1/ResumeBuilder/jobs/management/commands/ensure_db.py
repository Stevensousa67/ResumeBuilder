"""
Author: Steven Sousa
Prof.: John Santore
Institution: Bridgewater State University - COMP490 - Senior Design & Development
Version: 20Feb2025

Description: This script will make sure that the database is correctly setup so that Django can successfully connect
"""
# Import Dependencies
import psycopg
import os
from pathlib import Path
from decouple import AutoConfig
from django.core.management.base import BaseCommand
from django.db import connection

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
env_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_path):
    config = AutoConfig(search_path=BASE_DIR)

class Command(BaseCommand):
    help = 'Ensures that the database is correctly setup so that Django can successfully connect'

    def handle(self, *args, **options):
        # Get database credentials from .env
        db_name = config('DB_NAME')
        db_user = config('DB_USER')
        db_password = config('DB_PASSWORD')
        db_host = config('DB_HOST_DEFAULT')
        db_port = config('DB_PORT_DEFAULT')

        # Get default PostgreSQL credentials from .env
        db_name_default = config('DB_NAME_DEFAULT')
        db_user_default = config('DB_USER_DEFAULT')
        db_password_default = config('DB_PASSWORD_DEFAULT')

        # Connect to PostgreSQL server using default credentials
        try:
            with psycopg.connect(
                dbname=db_name_default,
                user=db_user_default,
                password=db_password_default,
                host=db_host,
                port=db_port,
                autocommit=True
            ) as conn:
                with conn.cursor() as cursor:
                    # Check if custom db exists in server
                    cursor.execute("""SELECT 1 FROM pg_database WHERE datname = %s;""", (db_name,))
                    if not cursor.fetchone():
                        # Create the database in the server
                        cursor.execute(f"CREATE DATABASE {db_name};")
                        self.stdout.write(self.style.SUCCESS(f"Database '{db_name}' created successfully."))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Database '{db_name}' already exists."))

                    # Check if custom user exists in server
                    cursor.execute("""SELECT 1 FROM pg_roles WHERE rolname = %s;""", (db_user,))
                    if not cursor.fetchone():
                        # Create the user in the server
                        cursor.execute(f"CREATE USER {db_user} WITH PASSWORD '{db_password}';")
                        self.stdout.write(self.style.SUCCESS(f"User '{db_user}' created successfully."))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"User '{db_user}' already exists."))
        except psycopg.OperationalError as e:
            self.stdout.write(self.style.ERROR(f"Error connecting to PostgreSQL server: {e}"))

        # Connect using the new credentials
        try:
            with psycopg.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""SELECT 1;""")
                    self.stdout.write(self.style.SUCCESS("Connection successful using new credentials!"))
        except psycopg.OperationalError as e:
            self.stdout.write(self.style.ERROR(f"Error connecting to PostgreSQL server using new credentials: {e}"))