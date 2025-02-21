from django.core.management.base import BaseCommand
from jobs.models import Job


class Command(BaseCommand):
    help = 'Imports jobs from existing PostgreSQL database table into django_jobs'

    def handle(self, *args, **options):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM jobs;")
            rows = cursor.fetchall()

            for row in rows:
                job_id = row[0]
                # Check if the job_id already exists in the database
                if not Job.objects.filter(job_id=job_id).exists():
                    Job.objects.create(
                        job_id=job_id,
                        job_title=row[1],
                        company_name=row[2],
                        job_description=row[3],
                        location=row[4],
                        min_salary=row[5],
                        max_salary=row[6],
                        salary_time=row[7],
                        posted_date=row[8],
                        url=row[9],
                        remote=row[10]
                    )

        self.stdout.write(self.style.SUCCESS(
            'Successfully imported jobs from the existing table into django_jobs, skipping duplicates'))
