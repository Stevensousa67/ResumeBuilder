from django.conf import settings
from candidate.models import Experience, Project, Reference
from google import genai


def extract_profile_data(profile):
    # Reused as-is (unchanged)
    user = profile.user
    profile_data = {
        'name': f"{user.first_name} {user.last_name}",
        'email': user.email,
        'phone': user.phone,
        'address': user.address if user.address else '',
        'website': user.website if user.website else '',
        'skills': user.skills if user.skills else '',
        'education': {
            'level': user.get_education_display() if user.education else '',
            'major': user.major if user.major else '',
            'courses': user.courses if user.courses else '',
        },
        'profile_name': profile.profile_name,
    }
    experiences = []
    for exp in Experience.objects.filter(profile=profile).order_by('-start_date'):
        experiences.append({
            'title': exp.title,
            'company': exp.company,
            'start_date': exp.start_date.strftime('%B %Y'),
            'end_date': exp.end_date.strftime('%B %Y') if exp.end_date else 'Present',
            'description': exp.description,
        })
    profile_data['experiences'] = experiences
    projects = []
    for proj in Project.objects.filter(profile=profile):
        projects.append({
            'title': proj.title,
            'description': proj.description,
        })
    profile_data['projects'] = projects
    references = []
    for ref in Reference.objects.filter(profile=profile):
        references.append({
            'name': f"{ref.first_name} {ref.last_name}",
            'phone': ref.phone if ref.phone else '',
            'email': ref.email if ref.email else '',
            'relationship': ref.relationship if ref.relationship else '',
        })
    profile_data['references'] = references
    return profile_data


def generate_content(profile, job, content_type):
    """
    Generate either a resume or a cover letter using Gemini API based on the content_type.

    Args:
        profile: The user's Profile instance.
        job: The Job instance for which the content is being generated.
        content_type: String, either "resume" or "cover_letter".

    Returns:
        str: The generated Markdown content.
    """
    if content_type not in ["resume", "cover_letter"]:
        raise ValueError("content_type must be 'resume' or 'cover_letter'")

    profile_data = extract_profile_data(profile)

    # Common prompt header
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

    # Tailor the prompt based on content_type
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

    # Get the raw Markdown content
    markdown_content = submit_prompt(prompt)

    # Strip code block markers if present
    if markdown_content.startswith("```markdown\n"):
        markdown_content = markdown_content[len("```markdown\n"):]
    if markdown_content.endswith("```"):
        markdown_content = markdown_content[:-3]

    return markdown_content.strip()


def submit_prompt(prompt):
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        if response and hasattr(response, 'text'):
            return response.text
        else:
            raise ValueError("Invalid response from Gemini API: No text content found")
    except Exception as e:
        raise Exception(f"Failed to generate content with Gemini API: {str(e)}")
