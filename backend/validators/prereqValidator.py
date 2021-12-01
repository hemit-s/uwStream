import re
import json
import requests
from backend.API_KEY import API_KEY

UWATERLOO_API_V3 = "https://openapi.data.uwaterloo.ca/v3"
STD_HEADER = {'x-api-key': API_KEY}


def get_current_term():
    requestURL = '{API}/Terms/current'.format(API=UWATERLOO_API_V3)
    response = requests.get(requestURL, headers=STD_HEADER)
    return response.json().get('termCode')


def get_course_details(subject, number):
    termCode = get_current_term()
    requestURL = '{API}/Courses/{term}/{sub}/{num}' \
                    .format(API=UWATERLOO_API_V3, 
                            term=termCode, 
                            sub=subject, 
                            num=number)
    response = requests.get(requestURL, headers=STD_HEADER)
    return response.json()[0]


def get_course_prereqs(course_details):
    subject = course_details.get('subjectCode')
    prereqs = []

    requirements = course_details.get('requirementsDescription')
    if requirements is None or not requirements.startswith('Prereq'):
        return prereqs

    reqs = re.split('; |\. ', requirements.split(': ')[1])
    while reqs and (reqs[-1] == 'Antireq' or reqs[-1] == 'Coreq'
                 or reqs[-1].endswith('only') or reqs[-1].endswith('students')
                 or reqs[-1].endswith('only.') or reqs[-1].endswith('students.')
                 or reqs[-1].endswith('Engineering') or reqs[-1].endswith('Engineering.')):
        reqs.pop()

    if not reqs:
        return prereqs

    ' '.join(reqs)

    prereqs = re.split(' and |, (?!(?:[^(]*\([^)]*\))*[^()]*\))', reqs) if not reqs.startswith('One of') else [reqs]

    return prereqs
