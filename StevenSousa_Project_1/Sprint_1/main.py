"""
Author: Steven Sousa
Prof.: John Santore
Institution: Bridgewater State University - COMP499 - Senior Design & Development
Version: 24Jan2025

Description: This program has the objective of submitting a prompt to Google AI Studio containing a job description,
information about myself, and ask it to return a sample resume in markdown format that will be designed for my skills
and the job description provided.
"""

# Import dependencies
import dotenv, os
import google.generativeai as genai
from google.generativeai.types import GenerateContentResponse


def load_Google_API_key() -> str | None:
    """
    Loads Google API key from .env file
    :return: api_key
    """
    dotenv.load_dotenv(os.path.join(os.path.dirname(os.getcwd()), '.env'))
    return os.getenv('GOOGLE_AI_API_KEY')


def setup_Google_Gemini(api_key: str) -> genai.GenerativeModel | None:
    """
    Setup Google Gemini Model
    :param api_key:
    :return: gemini-1.5-pro
    """
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-pro')

def create_prompt(job_description: str, my_info: str) -> GenerateContentResponse:
    """

    :param job_description:
    :param my_info:
    :return: Google AI Studio answer in markdown format
    """
    API_KEY = load_Google_API_key()
    model = setup_Google_Gemini(API_KEY)
    return model.generate_content([job_description, my_info, 'Generate a sample resume in markdown format that will be '
                                                             'designed for my skills and the job description provided.'])

job_description = ('Prototype, create, maintain, extend, and improve, and automate complex and flexible data-driven data '
                   'reporting and analysis tools used by the Research and Development groups in the U.S. and France and '
                   'by some production and support groups. Some of these tools already exist and use a combination of '
                   'Microsoft Excel (complex workbooks with complex formulas and VBA code/macros), Windows remote '
                   'applications, and web applications/APIs. We are also extending our tools\u2019 back-end in the '
                   'cloud, and you could be the one helping us in this endeavor.\n\nAs a Application Developer in the '
                   'clinical diagnostics group, daily activities will focus on improving existing web analysis tools '
                   'and deploying new features to streamline the flow and analysis of data in our organization. The '
                   'primary responsibilities are to maintain existing web-based applications in AWS and help to create '
                   'new applications as project needs evolve. A candidate passionate about improving healthcare, with '
                   'experience developing biological research tools and pipelines. The successful candidate will help '
                   'automate the analysis of routine experiments, develop algorithms, and perform statistical analysis '
                   'of biological datasets. A strong understanding of clinical laboratory testing methods is preferred.'
                   '\n\nHow You\u2019ll Make An Impact:\n\nWork with end users, both in technical and functional roles, '
                   'to gather requirements, develop solutions around them, and provide support as needed. This '
                   'includes:\n\u2022 Support manufacturing/production with data tools and support teams to ensure '
                   'their needs are met and that production can be performed as planned.\n\u2022 Using software '
                   'development tools and methodologies to maintain and improve good software development practices. '
                   'This includes writing, maintaining, and extending software documentation used for validation, '
                   'maintenance, and further development using software versioning tools.\n\u2022 Participating in an '
                   'agile development environment as well as ensuring that software solutions satisfy FDA and ISO '
                   'regulations.\n\u2022 Learning and/or using Labware ELN to support the day-to-day work in this '
                   'platform.\n\u2022 Coordinating with IT and other internal teams the testing, validation, and '
                   'promotion of developed solutions.\n\nWhat You Bring:\n\u2022 Education: BS or MS in Data Science, '
                   'computer science, or biological science; background in web application development.\n\u2022 '
                   'Work Experience: Perform analysis, design, coding, and testing for data-driven applications. '
                   'Solid software development background, a troubleshooting mindset, and good communication '
                   'skills.\n\u2022 Must be able to work throughout all the software development life cycle.\n\u2022 '
                   'Must be able to do technical documentation like impact analysis, test cases, etc.\n\u2022 '
                   'Must have software troubleshooting experience.\n\u2022 Must have experience with cloud computing '
                   'and database management in AWS.\n\u2022 Experience with HTTP based REST APIs and related web-based '
                   'protocols.\n\u2022 Strong programming skills in Python.\n\u2022 Experience with UI development '
                   '(HTML, CSS, Javascript, Angular).\n\u2022 Have a good understanding of software best practices, '
                   'development, test and deployment methodologies, and a variety of software tools. as well as an '
                   'understanding of source-control techniques and practices.\n\u2022 Have strong analytical '
                   'abilities.\n\u2022 Highly desirable candidates will also have:\n\u2022 An enthusiastic desire '
                   'toward learning new skills.\n\u2022 Capable of assisting users and triaging reported bugs.\n\u2022 '
                   'Experience working with Relational and NoSQL databases.\n\u2022 Be comfortable working with '
                   'multiple technologies across the full stack of an application (UI, business layer, configuration, '
                   'database).\n\u2022 Experience working in a highly regulated (e.g., FDA) environment, and/or '
                   'development experience in a biotech or Medical Device setting.\n\u2022 Understanding of Windows '
                   'domain (Active Directory) and Azure AD would be helpful (but not required).\n\u2022 Advanced '
                   'usage and understanding of Microsoft Office 365 or Microsoft 365 (VBA, Advanced formulas and '
                   'functions, Data Tables/List Objects).\n\nTotal Rewards Package: At Bio-Rad, we\u2019re empowered '
                   'by our purpose and recognize that our employees are as well. That\u2019s why we offer a competitive '
                   'and comprehensive Total Rewards Program that provides value, quality, and inclusivity while '
                   'satisfying the diverse needs of our evolving workforce. Bio-Rad\'s robust offerings serve to '
                   'enrich the overall health, wealth, and wellbeing of our employees and their families through the '
                   'various stages of an employee\u2019s work and life cycle.')

my_info = ('My name is Steven Sousa, I am a software engineer with a strong background in web development. My skills '
           'include HTML, CSS, JavaScript, Node.js, React, SQL (MySQL, PostgreSQL), Python, Django, Flask, MongoDB, AWS,'
           ' Docker, Git, CI/CD. I possess a B.S degree in Computer Science with no professional experience in software '
           'development, however, I have built and deployed various full-stack web applications. I am also proficient '
           'with Microsoft Office suite apps. I am a team player, a strong communicator, and a fast learner.')

response = create_prompt(job_description, my_info)
print(response.text)
