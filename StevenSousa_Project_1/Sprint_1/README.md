# Project Objectives
- Create a private github repo for this project
- Setup an API key for an LLM
- Send a prompt and retrieve the answer

# Why Google Gemini LLM?
I chose this LLM because I already had an account with Google, had previously utilized this LLM, and due to its ease 
of setting up.

# Prompt Construction
The prompts I chose are essentially 3:
1. Job Description: I hard-coded the first job description inside the rapid_jobs2.json file in its entirety, no changes made.
2. My Information: I provided some vague information about myself in order to protect my privacy.
3. Prompt: The prompt I settled on was passing the job description, my information, and response to be in markdown format. I settled on the current state because it provides enough vague information to tailor a favorable response. Of course, as more details about myself is added, the more detailed the response will be.

# Dependencies
- Python 3.9+, dotenv, os, re, google.generativeai, google.generativeai.types, API key for Gemini, markdown, xhtml2pdf

# How to install dependencies
- Python: https://www.python.org/downloads/
- os & re: standard python libraries, no need to pip install
- dotenv: pip install python-dotenv
- google.generativeai: pip install -q -U google-generativeai
- markdown: pip install markdown
- xhtml2pdf: pip install xhtml2pdf
- API key located in .env file

# How to Run

Once all dependencies have been installed, simply run the main.py file. The Gemini response will appear in the terminal.
I have hard coded the job description, information about myself, and what to return. Should you want a different job
description, simply look for "description" key in the rapid_jobs2.json file, copy it's content, and paste into the 
job_description variable. Additionally, the program will save the pdf version of the response called "Steven Sousa - Resume".

# Sample Input

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

prompt to gemini: Generate a sample resume in markdown format that will be designed for my skills and the job 
description provided.'

# Sample output:

# Steven Sousa
(123) 456-7890 | steven.sousa@email.com | linkedin.com/in/steven-sousa | github.com/yourgithubusername

## Summary

Highly motivated and skilled software engineer with a strong foundation in web development and a passion for leveraging technology to improve healthcare.  Proficient in a range of front-end and back-end technologies, including Python, JavaScript, React, SQL, and AWS.  Eager to apply my skills to develop and maintain data-driven applications in a collaborative, regulated environment like Bio-Rad's clinical diagnostics group.

## Skills

**Programming Languages:** Python, JavaScript, SQL, HTML, CSS, VBA
**Frameworks/Libraries:** React, Node.js, Django, Flask, Angular
**Databases:** MySQL, PostgreSQL, MongoDB
**Cloud Computing:** AWS (mention specific services if familiar, e.g., S3, EC2, Lambda)
**Tools:** Docker, Git, CI/CD, Microsoft Office Suite (Excel, Word, PowerPoint), Microsoft 365
**Methodologies:** Agile, Software Development Life Cycle (SDLC)

## Projects

*(Replace with 2-3 of your most relevant projects.  Quantify your accomplishments whenever possible.)*

* **Project Title 1:**  Briefly describe the project and your role.  Highlight technologies used and key results. *Example: Developed a full-stack web application for [purpose] using React, Node.js, and PostgreSQL.  Improved user engagement by 20%.*
* **Project Title 2:**  Briefly describe the project and your role. Highlight technologies used and key results. *Example:  Built a data pipeline to automate data collection and analysis using Python and AWS Lambda. Reduced processing time by 50%.*
* **Project Title 3:** Briefly describe the project and your role. Highlight technologies used and key results.  *Example: Created a data visualization dashboard using D3.js to provide insights into [data].*


## Education

**B.S. in Computer Science** | University Name | Year of Graduation


## Awards and Recognition

*(Optional: List any relevant awards or recognitions)*


## Relevant Coursework

*(Optional: List relevant coursework, especially if you lack professional experience.  Focus on courses that align with the job description, such as database management, software engineering principles, algorithms, bioinformatics, etc.)*


## Extracurricular Activities

*(Optional:  Include any relevant extracurricular activities, such as participation in hackathons or coding clubs.)*


---

**Tailoring Your Resume:**

* **Keywords:** Carefully review the job description and incorporate relevant keywords throughout your resume.  This will help your resume get noticed by applicant tracking systems (ATS).
* **Quantify:**  Use numbers and metrics to demonstrate the impact of your work.
* **Microsoft Office Skills:**  Since the job description emphasizes Microsoft Office proficiency, provide specific examples of your advanced skills (e.g., "Developed complex Excel workbooks with VBA macros to automate data analysis for [project]").
* **Enthusiasm:**  Highlight your passion for learning and contributing to healthcare, as mentioned in the job description.
* **Cover Letter:** Write a compelling cover letter that connects your skills and experience to the specific requirements of the role.  Address your lack of professional experience by emphasizing your project work, relevant coursework, and eagerness to learn.
```

This resume format provides a strong foundation for your application.  Remember to customize it further based on the specific requirements of the job posting and highlight the projects and skills that best align with Bio-Rad's needs. Good luck!
