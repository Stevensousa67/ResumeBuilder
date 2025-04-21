from django.test import TransactionTestCase
from candidate.models import User, Profile, Experience
from jobs.models import Job
from gemini.services.gemini_api import extract_profile_data
from gemini.services.pdf_service import convert_markdown_to_pdf
import uuid
import datetime as date
import io
import sys
from google import genai
from decouple import config


class TestGeminiApp(TransactionTestCase):
    def setUp(self):
        self.stdout = io.StringIO()
        sys.stdout = self.stdout

        # Set Gemini API key using decouple
        self.gemini_api_key = config('GEMINI_API_KEY')
        if not self.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. Set it via GitHub Secrets or .env file.")

        # Create a unique test user for each test run
        unique_email = f"testuser_{uuid.uuid4()}@example.com"
        self.user = User.objects.create_user(
            username=unique_email,
            email=unique_email,
            password='Password123!',
            first_name='Test',
            last_name='User',
            phone='1234567890',
            address='123 Main St.',
            skills='Python, Django',
            education='Bachelor',
            major='Computer Science',
            courses='CS101, CS201'
        )

        # Create a test profile with some data
        self.profile = Profile.objects.create(
            user=self.user,
            profile_name='TestProfile',
        )

        # Create a test job
        self.job = Job.objects.create(
            job_id='TEST123',
            job_title='Python Developer',
            company_name='Test Company',
            job_description='Looking for a Python developer with Django experience.',
            location='Test Location',
            remote=True,
            min_salary=50000,
            max_salary=60000,
            salary_time='yearly',
            posted_date=date.datetime.now(),
            url='http://test.com'
        )

        # Create test experience
        Experience.objects.create(
            profile=self.profile,
            title='Python Developer',
            company='Old Company',
            start_date=date.datetime.now() - date.timedelta(days=365),
            description='Developed web apps with Django'
        )

        # Log in the user for the test
        self.client.force_login(self.user)

    def tearDown(self):
        print(self.stdout.getvalue())
        sys.stdout = sys.__stdout__
        self.user.delete()

    def test_01_LLM_200_status(self):
        """
        Test that the Gemini API returns a 200 status code when queried directly.
        Note: This test makes a real API call. Ensure GEMINI_API_KEY is set.
        """
        # Simple prompt to test the API
        prompt = "Test prompt to verify API status"

        try:
            client = genai.Client(api_key=self.gemini_api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            # Check if the response is successful
            self.assertIsNotNone(response, "API response should not be None")
            self.assertTrue(hasattr(response, 'text'), "Response should have text attribute")
            self.assertGreater(len(response.text), 0, "Response text should not be empty")

            print("API call successful. Response text:", response.text)

        except Exception as e:
            self.fail(f"Gemini API call failed with error: {str(e)}")

    def test_02_prompt_contains_job_and_user_info(self):
        """
        Test that the automatically created prompt contains both the job description
        and user information.
        """
        # Generate the profile data using the same function as gemini_api.py
        profile_data = extract_profile_data(self.profile)
        job = self.job

        # Reconstruct the prompt exactly as in gemini_api.py
        content_type = "resume"  # Match the content type used in gemini_api.py
        prompt = f"""
    Please create a professional {content_type} for a candidate applying for the following job:

    Job Title: {job.job_title}
    Company: {job.company_name}
    Job Description: {job.job_description}

    Here's the candidate's profile information:

    PERSONAL INFORMATION:
    Name: {profile_data['name']}
    Email: {profile_data['email']}
    Phone: {profile_data['phone']}
    Address: {profile_data['address']}
    Website: {profile_data['website']}

    EDUCATION:
    Level: {profile_data['education']['level']}
    Major: {profile_data['education']['major']}

    SKILLS:
    {profile_data['skills']}

    COURSES:
    {profile_data['education']['courses']}

    EXPERIENCE:
    """
        if not profile_data['experiences']:
            prompt += "No work experience available"
        else:
            for exp in profile_data['experiences']:
                prompt += f"""
    {exp['title']} at {exp['company']}
    {exp['start_date']} - {exp['end_date']}
    {exp['description']}
    """

        prompt += """
    PROJECTS:
    """
        if not profile_data['projects']:
            prompt += "No projects available"
        else:
            for proj in profile_data['projects']:
                prompt += f"""
    {proj['title']}
    {proj['description']}
    """

        prompt += """
    REFERENCES:
    """
        if not profile_data['references']:
            prompt += "No references available"
        else:
            for ref in profile_data['references']:
                prompt += f"""
    {ref['name']}
    Phone: {ref['phone']}
    Email: {ref['email']}
    Relationship: {ref['relationship']}
    """

        prompt += f"""
                Please format this information into a professional {content_type} tailored specifically for this job.
                Highlight the skills and experiences that are most relevant to the job description.
                The {content_type} should be concise, well-organized\
                {' and include a formal salutation and closing' if content_type == 'cover_letter' else ''}.
                Use only the provided information listed in the prompt - don't add any additional details.
                Omit skills and projects that don't support this job description.
                Return the {content_type} in markdown format without any additional notes or extra cruft.
                I want just the {content_type}.
                """

        # Assert that the prompt contains job description and user information
        self.assertIn(job.job_description, prompt, "Prompt should contain job description")
        self.assertIn(profile_data['name'], prompt, "Prompt should contain user name")
        self.assertIn(profile_data['email'], prompt, "Prompt should contain user email")
        self.assertIn(profile_data['phone'], prompt, "Prompt should contain user phone")
        self.assertIn(profile_data['skills'], prompt, "Prompt should contain user skills")
        if profile_data['experiences']:
            self.assertIn(profile_data['experiences'][0]['title'], prompt, "Prompt should contain experience title")

    def test_03_convert_markdown_to_pdf_valid_input(self):
        """
        Test that convert_markdown_to_pdf successfully converts valid Markdown to PDF.
        """
        # Sample Markdown content
        markdown_content = """
    # Test Resume
    **Name:** Test User

    ## Experience
    - **Python Developer** at Old Company
      - Developed web apps with Django
    """

        # Call the function
        pdf_content = convert_markdown_to_pdf(markdown_content)

        # Assert the PDF content is non-empty
        self.assertIsNotNone(pdf_content, "PDF content should not be None")
        self.assertGreater(len(pdf_content), 0, "PDF content should not be empty")

        # Check if the content looks like a PDF (starts with %PDF-)
        pdf_header = pdf_content[:5].decode('latin1')
        self.assertTrue(pdf_header.startswith('%PDF-'), "Output should start with %PDF- header")

    def test_04_convert_markdown_to_pdf_empty_input(self):
        """
        Test that convert_markdown_to_pdf handles empty Markdown input gracefully.
        """
        markdown_content = ""

        # Call the function (should still produce a PDF, just with minimal content)
        pdf_content = convert_markdown_to_pdf(markdown_content)

        # Assert the PDF content is non-empty
        self.assertIsNotNone(pdf_content, "PDF content should not be None")
        self.assertGreater(len(pdf_content), 0, "PDF content should not be empty")

        # Check if the content looks like a PDF
        pdf_header = pdf_content[:5].decode('latin1')
        self.assertTrue(pdf_header.startswith('%PDF-'), "Output should start with %PDF- header")
