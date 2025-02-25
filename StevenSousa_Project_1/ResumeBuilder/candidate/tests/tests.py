import json
from django.test import TransactionTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from candidate.models import Candidate, Experience, Project, Reference
from bs4 import BeautifulSoup
import datetime as date
import sys
import io
import uuid


class TestCandidateDatabase(TransactionTestCase):
    def setUp(self):
        self.stdout = io.StringIO()
        sys.stdout = self.stdout

        # Create a unique test user for each test run
        unique_email = f"testuser_{uuid.uuid4()}@example.com"
        self.user = User.objects.create_user(
            username=unique_email,
            email=unique_email,
            password='Password123!'
        )
        # Create a valid Candidate object
        self.candidate = Candidate.objects.create(
            user=self.user,
            email=self.user.email,
            first_name="Initial",
            last_name="User",
            phone="1234567890"
        )

    def tearDown(self):
        print(self.stdout.getvalue())
        sys.stdout = sys.__stdout__
        self.user.delete()
        Candidate.objects.all().delete()
        Experience.objects.all().delete()
        Project.objects.all().delete()
        Reference.objects.all().delete()

    def test_01_candidate_signup(self):
        client = self.client
        url = reverse('candidate:signup')

        unique_email = f"testuser_{uuid.uuid4()}@example.com"
        data = {
            'email': unique_email,
            'password': 'Password123!',
            'password_confirm': 'Password123!',
        }
        response = client.post(url, data)

        self.assertEqual(response.status_code, 302, 'User was redirected')
        self.assertTrue(User.objects.filter(email=data['email']).exists(), 'User was created')
        self.assertTrue(Candidate.objects.filter(email=data['email']).exists(), 'Candidate was created')

        candidate = Candidate.objects.get(email=data['email'])
        self.assertEqual(candidate.email, data['email'], 'Candidate email matches')
        self.assertEqual(candidate.first_name, '', 'Candidate first name is empty')
        self.assertEqual(candidate.last_name, '', 'Candidate last name is empty')
        self.assertEqual(candidate.phone, '', 'Candidate phone is empty')
        self.assertIsNone(candidate.website, 'Candidate website is empty')
        self.assertIsNone(candidate.skills, 'Candidate skills is empty')
        self.assertIsNone(candidate.address, 'Candidate address is empty')
        self.assertIsNone(candidate.education, 'Candidate education is empty')
        self.assertIsNone(candidate.major, 'Candidate major is empty')
        self.assertIsNone(candidate.courses, 'Candidate courses is empty')

    def test_02_candidate_update(self):
        client = self.client

        # Login the user
        self.assertTrue(client.login(username=self.user.username, password='Password123!'), 'User logged in')

        url = reverse('candidate:edit_user')

        # Initialize the wizard
        response = client.get(url)
        self.assertEqual(response.status_code, 200, "Wizard page should load successfully")

        # Extract the CSRF token and hash or hidden fields from the GET response using BeautifulSoup
        soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
        csrf_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        csrf_value = csrf_input['value'] if csrf_input else ''

        # Step 1 - Update candidate profile
        candidate_data = {
            'candidate-first_name': 'Test',
            'candidate-last_name': 'User',
            'candidate-email': self.user.email.lower(),
            'candidate-phone': '5555555555',
            'candidate-website': 'https://www.example.com',
            'candidate-address': '1234 Elm St, Springfield, IL 62701',
            'candidate-education': 'BA',
            'candidate-major': 'Computer Science',
            'candidate-skills': 'Python, Django, JavaScript',
            'candidate-courses': 'Data Structures, Algorithms, Web Development',
            'edit_user_wizard-current_step': 'candidate',
            'csrfmiddlewaretoken': csrf_value,
        }
        response = client.post(url, candidate_data)
        self.assertEqual(response.status_code, 200, "Should redirect to next step")
        self.assertContains(response, '<h2 class="h4 mb-3">Experience</h2>', html=True,
                            msg_prefix="Next step should be Experience")

        # Step 2 - Update candidate experiences
        experience_data = {
            'experiences-0-title': 'Software Developer',
            'experiences-0-company': 'Example Corp',
            'experiences-0-start_date': '2025-01-01',
            'experiences-0-end_date': '',
            'experiences-0-description': 'Developed software applications for clients',
            'experiences-0-id': '',
            'experiences-TOTAL_FORMS': '1',
            'experiences-INITIAL_FORMS': '0',
            'experiences-MIN_NUM_FORMS': '0',
            'experiences-MAX_NUM_FORMS': '1000',
            'edit_user_wizard-current_step': 'experience',
            'csrfmiddlewaretoken': csrf_value,
        }
        response = client.post(url, experience_data)
        self.assertEqual(response.status_code, 200, "Should redirect to next step")
        self.assertContains(response, '<h2 class="h4 mb-3">Projects</h2>', html=True,
                            msg_prefix="Next step should be Experience")

        # Step 3 - Update candidate projects
        project_data = {
            'projects-0-title': 'Project A',
            'projects-0-description': 'Developed a web application for tracking inventory',
            'projects-0-id': '',
            'projects-TOTAL_FORMS': '1',
            'projects-INITIAL_FORMS': '0',
            'projects-MIN_NUM_FORMS': '0',
            'projects-MAX_NUM_FORMS': '1000',
            'edit_user_wizard-current_step': 'projects',
            'csrfmiddlewaretoken': csrf_value,
        }
        response = client.post(url, project_data)
        self.assertEqual(response.status_code, 200, "Should redirect to next step")
        self.assertContains(response, '<h2 class="h4 mb-3">References</h2>', html=True,
                            msg_prefix="Next step should be Experience")

        # Step 4 - Update candidate references
        reference_data = {
            'references-0-first_name': 'Jane',
            'references-0-last_name': 'Smith',
            'references-0-phone': '9876543210',
            'references-0-email': 'jane@example.com',
            'references-0-relationship': 'Colleague',
            'references-0-id': '',
            'references-TOTAL_FORMS': '1',
            'references-INITIAL_FORMS': '0',
            'references-MIN_NUM_FORMS': '0',
            'references-MAX_NUM_FORMS': '1000',
            'edit_user_wizard-current_step': 'references',
            'csrfmiddlewaretoken': csrf_value,
        }
        response = client.post(url, reference_data)
        self.assertEqual(response.status_code, 302, "Should redirect to jobs_list after completing wizard")

        # Verify the candidate record has updated data
        candidate = Candidate.objects.get(user=self.user)
        self.assertEqual(candidate.first_name, candidate_data['candidate-first_name'], 'Candidate first name matches')
        self.assertEqual(candidate.last_name, candidate_data['candidate-last_name'], 'Candidate last name matches')
        self.assertEqual(candidate.phone, candidate_data['candidate-phone'], 'Candidate phone matches')
        self.assertEqual(candidate.website, candidate_data['candidate-website'], 'Candidate website matches')
        self.assertEqual(candidate.skills, candidate_data['candidate-skills'], 'Candidate skills matches')
        self.assertEqual(candidate.address, candidate_data['candidate-address'], 'Candidate location matches')
        self.assertEqual(candidate.education, candidate_data['candidate-education'], 'Candidate education matches')
        self.assertEqual(candidate.major, candidate_data['candidate-major'], 'Candidate major matches')
        self.assertEqual(candidate.courses, candidate_data['candidate-courses'], 'Candidate courses matches')

        # Verify the experiences record has updated data
        experiences = Experience.objects.filter(candidate=candidate)
        self.assertEqual(len(experiences), 1)
        experience = experiences[0]
        self.assertEqual(experience.title, experience_data['experiences-0-title'], 'Experience title matches')
        self.assertEqual(experience.company, experience_data['experiences-0-company'], 'Experience company matches')
        self.assertEqual(experience.start_date, date.date(2025, 1, 1), 'Experience start date matches')
        self.assertIsNone(experience.end_date, 'Experience end date should be None')
        self.assertEqual(experience.description, experience_data['experiences-0-description'],
                         'Experience description matches')

        # Verify the projects record has updated data
        projects = Project.objects.filter(candidate=candidate)
        self.assertEqual(len(projects), 1)
        project = projects[0]
        self.assertEqual(project.title, project_data['projects-0-title'], 'Project title matches')
        self.assertEqual(project.description, project_data['projects-0-description'], 'Project description matches')

        # Verify the references record has updated data
        references = Reference.objects.filter(candidate=candidate)
        self.assertEqual(len(references), 1)
        reference = references[0]
        self.assertEqual(reference.first_name, reference_data['references-0-first_name'],
                         'Reference first name matches')
        self.assertEqual(reference.last_name, reference_data['references-0-last_name'], 'Reference last name matches')
        self.assertEqual(reference.phone, reference_data['references-0-phone'], 'Reference phone matches')
        self.assertEqual(reference.email, reference_data['references-0-email'], 'Reference email matches')
        self.assertEqual(reference.relationship, reference_data['references-0-relationship'],
                         'Reference relationship matches')