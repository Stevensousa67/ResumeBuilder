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
from decouple import config, AutoConfig
from django.core.management.base import BaseCommand

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
env_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_path):
    env_config = AutoConfig(search_path=BASE_DIR)


class Command(BaseCommand):
    help = 'Verifies that Django can connect to the Supabase PostgreSQL database'

    def handle(self, *args, **options):
        # Get database credentials from .env (Supabase credentials)
        db_name = config('SUPABASE_DB_NAME')
        db_user = config('SUPABASE_USER')
        db_password = config('SUPABASE_PASSWORD')
        db_host = config('SUPABASE_HOST')
        db_port = config('SUPABASE_PORT')

        # Attempt to connect to the Supabase database
        try:
            with psycopg.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1;")
                    self.stdout.write(self.style.SUCCESS(f"Successfully connected to '{db_name}' database!"))
        except psycopg.OperationalError as e:
            self.stdout.write(self.style.ERROR(f"Error connecting to Supabase database: {e}"))