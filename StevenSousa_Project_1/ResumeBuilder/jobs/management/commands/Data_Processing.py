"""
Author: Steven Sousa
Prof.: John Santore
Institution: Bridgewater State University - COMP490 - Senior Design & Development
Version: 20Feb2025

This file will parse the json files containing jobs and save them to the Django managed DB.
"""
# Import dependencies
import json
import re
from django.core.management.base import BaseCommand
from jobs.models import Job

class Command(BaseCommand):
    help = 'Parses job data from JSON files and saves it to the Django managed DB.'

    def handle(self, *args, **options):
        insert_count = 0
        json_files = ['../data/rapidResults.json', '../data/rapid_jobs2.json']

        for filename in json_files:
            with open(filename, 'r') as file:
                for line in file:
                    try:
                        data = json.loads(line.strip())
                        job_objects = self.normalize_json_data(data)
                        for obj in job_objects:
                            job_data = self.extract_job_data(obj)
                            Job.objects.update_or_create(
                                job_id = job_data['job_id'],
                                defaults={
                                    'job_title': job_data['job_title'],
                                    'company_name': job_data['company_name'],
                                    'job_description': job_data['job_description'],
                                    'location': job_data['location'],
                                    'min_salary': job_data['min_salary'],
                                    'max_salary': job_data['max_salary'],
                                    'salary_time': job_data['salary_time'],
                                    'posted_date': job_data['posted_date'],
                                    'url': job_data['url'],
                                    'remote': job_data['remote']
                                }
                            )
                            insert_count += 1
                    except json.JSONDecodeError as e:
                        self.stdout.write(self.style.ERROR(f"Error decoding JSON: {e}"))
        self.stdout.write(self.style.SUCCESS(f"Successfully inserted {insert_count} jobs to the database."))


    def normalize_json_data(self, data):
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
        else:
            self.stdout.write(self.style.ERROR(f"Skipping invalid data structure: {data}"))
            return []


    def extract_job_data(self, obj):
        return {
            'job_id': obj.get('id', 'N/A'),
            'job_title': obj.get('title', 'N/A'),
            'company_name': obj.get('company', 'N/A'),
            'job_description': obj.get('description', 'N/A'),
            'location': obj.get('location', 'N/A'),
            'min_salary': self.parse_salary(obj)[0],
            'max_salary': self.parse_salary(obj)[1],
            'salary_time': self.get_salary_frequency(obj),
            'posted_date': obj.get('datePosted', obj.get('date_posted', 'N/A')),
            'url': self.get_url(obj),
            'remote': self.get_remote_status(obj),
        }


    def parse_salary(self, job_obj):
        if 'min_amount' and 'max_amount' in job_obj:
            min_salary = self.convert_salary(job_obj['min_amount'])
            max_salary = self.convert_salary(job_obj['max_amount'])
            return min_salary, max_salary

        salary_range = job_obj.get('salaryRange', '')
        if salary_range:
            numbers = re.findall(r'[\d,]+K?|\d+', salary_range)
            salaries = []
            for num in numbers:
                num = num.replace(',', '')
                if num.endswith('K'):
                    salaries.append(int(float(num[:-1]) * 1000))
                else:
                    salaries.append(int(num))

            if len(salaries) == 2:
                return salaries[0], salaries[1]
            elif len(salaries) == 1:
                return salaries[0], salaries[0]
        return 0, 0


    def convert_salary(self, salary):
        if salary != '':
            return int(float(salary))
        else:
            return 0


    def get_salary_frequency(self, job_obj):
        if 'salaryRange' in job_obj:
            if 'hour' in job_obj['salaryRange']:
                return 'hourly'
            elif 'year' in job_obj['salaryRange'] or job_obj['salaryRange'] == '':
                return 'yearly'
        elif 'interval' in job_obj:
            return 'yearly' if job_obj['interval'] == '' else job_obj['interval']
        return 'yearly'

    def get_url(self, job_obj):
        if 'jobProviders' in job_obj:
            job_providers = job_obj.get('jobProviders', [])
            return job_providers[0].get('url', 'URL Not Found') if job_providers else 'URL Not Found'
        elif 'job_url' in job_obj:
            return job_obj.get('job_url', 'URL Not Found')
        return 'URL Not Found'


    def get_remote_status(self, job_obj):
        if 'is_remote' in job_obj:
            return False if job_obj['is_remote'] == '' else job_obj['is_remote']
        elif 'location' in job_obj:
            return True if 'remote' in job_obj['location'].lower() or 'remote' in job_obj['title'] else False
        return False
