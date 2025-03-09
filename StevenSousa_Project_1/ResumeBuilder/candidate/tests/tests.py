from django.test import TransactionTestCase
from django.urls import reverse
from candidate.models import User, Profile, Experience, Project, Reference
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
            password='Password123!',
            first_name='Test',
            last_name='User',
            phone='1234567890'
        )

    def tearDown(self):
        print(self.stdout.getvalue())
        sys.stdout = sys.__stdout__
        self.user.delete()
        Profile.objects.all().delete()
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

        # Verify that no profile is created at signup
        user = User.objects.get(email=data['email'])
        self.assertFalse(Profile.objects.filter(user=user).exists(), 'Profile was not created')
        self.assertEqual(user.email, data['email'], 'User email matches')
        self.assertEqual(user.first_name, '', 'User first name is empty')
        self.assertEqual(user.last_name, '', 'User last name is empty')
        self.assertEqual(user.phone, '', 'User phone is empty')
        self.assertIsNone(user.website, 'User website is empty')
        self.assertIsNone(user.skills, 'User skills is empty')
        self.assertIsNone(user.address, 'User address is empty')
        self.assertIsNone(user.education, 'User education is empty')
        self.assertIsNone(user.major, 'User major is empty')
        self.assertIsNone(user.courses, 'User courses is empty')

    def test_02_candidate_update(self):
        client = self.client

        # Login the user
        self.assertTrue(client.login(username=self.user.username, password='Password123!'), 'User logged in')

        url = reverse('candidate:edit_user')

        # Initialize the wizard
        response = client.get(url)
        self.assertEqual(response.status_code, 200, "Wizard page should load successfully")

        # Extract the CSRF token
        soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
        csrf_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        csrf_value = csrf_input['value'] if csrf_input else ''

        # Step 1 - Update user profile
        user_data = {
            'user-first_name': 'Test',
            'user-last_name': 'User',
            'user-email': self.user.email.lower(),
            'user-phone': '5555555555',
            'user-website': 'https://www.example.com',
            'user-address': '1234 Elm St, Springfield, IL 62701',
            'user-education': 'BS',  # Fixed: changed from 'BA' to match model choices
            'user-major': 'Computer Science',
            'user-skills': 'Python, Django, JavaScript',
            'user-courses': 'Data Structures, Algorithms, Web Development',
            'edit_user_wizard-current_step': 'user',
            'csrfmiddlewaretoken': csrf_value,
        }
        response = client.post(url, user_data)
        self.assertEqual(response.status_code, 200, "Should redirect to next step")
        self.assertContains(response, '<h2 class="h4 mb-3">Profile Options</h2>', html=True,
                            msg_prefix="Next step should be Profile Options")

        # Step 2 - Select "new" profile option and create a new profile
        profile_data = {
            'profile_select-profile_option': 'new',  # Selects the radio button for new profile
            'profile_select-new_profile_name': 'Software Developer',  # Enters new profile name
            'edit_user_wizard-current_step': 'profile_select',
            'csrfmiddlewaretoken': csrf_value,
        }
        response = client.post(url, profile_data)
        self.assertEqual(response.status_code, 200, "Should redirect to next step")
        self.assertContains(response, '<h2 class="h4 mb-3">Experience</h2>', html=True,
                            msg_prefix="Next step should be Experience")

        # Step 3 - Update candidate experiences
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
                            msg_prefix="Next step should be Projects")

        # Step 4 - Update candidate projects
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
                            msg_prefix="Next step should be References")

        # Step 5 - Update candidate references
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

        # Verify the user record has updated data
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.first_name, user_data['user-first_name'], 'User first name matches')
        self.assertEqual(user.last_name, user_data['user-last_name'], 'User last name matches')
        self.assertEqual(user.phone, user_data['user-phone'], 'User phone matches')
        self.assertEqual(user.website, user_data['user-website'], 'User website matches')
        self.assertEqual(user.skills, user_data['user-skills'], 'User skills matches')
        self.assertEqual(user.address, user_data['user-address'], 'User location matches')
        self.assertEqual(user.education, user_data['user-education'], 'User education matches')
        self.assertEqual(user.major, user_data['user-major'], 'User major matches')
        self.assertEqual(user.courses, user_data['user-courses'], 'User courses matches')

        # Verify the profile was created
        self.assertEqual(Profile.objects.filter(user=user).count(), 1, 'One profile should exist')
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.profile_name, profile_data['profile_select-new_profile_name'], 'Profile name matches')

        # Verify the experiences record has updated data
        experiences = Experience.objects.filter(profile=profile)  # Fixed: changed 'candidate' to 'profile'
        self.assertEqual(len(experiences), 1)
        experience = experiences[0]
        self.assertEqual(experience.title, experience_data['experiences-0-title'], 'Experience title matches')
        self.assertEqual(experience.company, experience_data['experiences-0-company'], 'Experience company matches')
        self.assertEqual(experience.start_date, date.date(2025, 1, 1), 'Experience start date matches')
        self.assertIsNone(experience.end_date, 'Experience end date should be None')
        self.assertEqual(experience.description, experience_data['experiences-0-description'],
                         'Experience description matches')

        # Verify the projects record has updated data
        projects = Project.objects.filter(profile=profile)  # Fixed: changed 'candidate' to 'profile'
        self.assertEqual(len(projects), 1)
        project = projects[0]
        self.assertEqual(project.title, project_data['projects-0-title'], 'Project title matches')
        self.assertEqual(project.description, project_data['projects-0-description'], 'Project description matches')

        # Verify the references record has updated data
        references = Reference.objects.filter(profile=profile)  # Fixed: changed 'candidate' to 'profile'
        self.assertEqual(len(references), 1)
        reference = references[0]
        self.assertEqual(reference.first_name, reference_data['references-0-first_name'],
                         'Reference first name matches')
        self.assertEqual(reference.last_name, reference_data['references-0-last_name'],
                         'Reference last name matches')
        self.assertEqual(reference.phone, reference_data['references-0-phone'], 'Reference phone matches')
        self.assertEqual(reference.email, reference_data['references-0-email'], 'Reference email matches')
        self.assertEqual(reference.relationship, reference_data['references-0-relationship'],
                         'Reference relationship matches')
