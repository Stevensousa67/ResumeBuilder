"""
Author: Steven Sousa
Prof.: John Santore
Institution: Bridgewater State University - COMP490 - Senior Design & Development
Version: 09Feb2025

Description: This program will receive the parameters from main.py, construct a prompt, and send it to Google AI Studio.
"""
# from google.generativeai import genai
#
#
# def generate_resume(
#         api_key: str,
#         job_description: str,
#         contact_info: str,
#         skills: str,
#         education: str,
#         experience: str,
#         refs: str,
#         constraints: str,
# ):
#     client = genai.Client(api_key)
#     prompt = f"""Build a markdown resume for me utilizing the following job description: {job_description},
#     contact information: {contact_info}, skills: {skills}, education: {education},
#     professional experience: {experience}, and professional references: {refs}, keeping in mind the following
#     constraints: {constraints}, """
#
#     response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
#
#     with open("Steven Sousa - Resume.md", "w") as file:
#         file.write(response.text[9:-3])
