import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box


console = Console()

def print_banner():
    banner_text = """

                                                                         
 _____ _____ _____ _____    _____ _____ _____    _____ _____ _____ _____ 
|  _  |  |  |_   _|     |  |     |   __|     |  |   __|     | __  |     |
|     |  |  | | | |  |  |  |  |  |   __|   --|  |   __|  |  |    -| | | |
|__|__|_____| |_| |_____|  |__  _|_____|_____|  |__|  |_____|__|__|_|_|_|
                              |__|                                       

                                                                                                                
    """
    console.print(banner_text, style="bold blue")

print_banner()

print("Developer instagram : _mohmdawais\n\n\n\n")

# Ask user for their login credentials
username = input("Enter your ID: ")
password = input("Enter your password: ")

# Define the URLs
login_url = "https://portals.au.edu.pk/qec/login.aspx"
base_url = "https://portals.au.edu.pk/qec/"
first_performa_url = base_url + "p1.aspx"
teacher_evaluation_url = base_url + "p10.aspx"
online_learning_feedback_url = base_url + "p10a_learning_online_form.aspx"

# Start a session
session = requests.Session()

# Get the login page to retrieve hidden form fields
response = session.get(login_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract hidden form fields
viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
viewstategenerator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']

# Prepare the payload for the login POST request
payload = {
    'ctl00$ContentPlaceHolder2$ddlcampus': 'Islamabad',
    'ctl00$ContentPlaceHolder2$ddlUserType': 'Student/Alumni',
    'ctl00$ContentPlaceHolder2$txt_regid': username,
    'ctl00$ContentPlaceHolder2$txt_password': password,
    'ctl00$ContentPlaceHolder2$btnAccountlogin': 'Login',
    '__VIEWSTATE': viewstate,
    '__EVENTVALIDATION': eventvalidation,
    '__VIEWSTATEGENERATOR': viewstategenerator
}

# Perform the login
login_response = session.post(login_url, data=payload)

# Check if login was successful
if "logout" in login_response.text.lower():
    console.print("\n\n[ ✔  ] Login successful", style="bold green")
else:
    console.print("[ ✘  ] Login failed", style="bold red")
    exit()

# Function to update hidden fields
def update_hidden_fields(soup):
    return (soup.find('input', {'name': '__VIEWSTATE'})['value'],
            soup.find('input', {'name': '__EVENTVALIDATION'})['value'],
            soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value'])

# Navigate to the first proforma
response = session.get(first_performa_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the subjects dropdown and get the list of subjects
subjects_dropdown = soup.find('select', {'name': 'ctl00$ContentPlaceHolder2$cmb_courses'})
subjects = subjects_dropdown.find_all('option')[1:]  # Skipping the first option which is the placeholder

# Check if there are no subjects available
if not subjects:
    console.print("[ ✔  ] Courses QEC form already filled", style="bold yellow")
else:
    # Iterate over each subject and fill out the form
    for subject in subjects:
        subject_value = subject['value']

        # Select the subject
        payload = {
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder2$cmb_courses',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstategenerator,
            '__EVENTVALIDATION': eventvalidation,
            'ctl00$ContentPlaceHolder2$cmb_courses': subject_value,
        }

        response = session.post(first_performa_url, data=payload)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Update hidden form fields after selecting the subject
        viewstate, eventvalidation, viewstategenerator = update_hidden_fields(soup)

        # Prepare the payload for submitting the proforma
        form_payload = {
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstategenerator,
            '__EVENTVALIDATION': eventvalidation,
            'ctl00$ContentPlaceHolder2$q1': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q2': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q3': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q4': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q5': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q6': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q7': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q8': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q9': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q10': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q11': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q12': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$btnSave': 'Submit Proforma',
        }

        submit_response = session.post(first_performa_url, data=form_payload)
        print(f"[*] Submitted proforma for subject {subject.text}")

    console.print("[ ✔  ] All subjects processed.", style="bold green")

# Navigate to the Teacher Evaluation Form
response = session.get(teacher_evaluation_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract hidden form fields for the teacher evaluation form
viewstate, eventvalidation, viewstategenerator = update_hidden_fields(soup)

# Find the teachers dropdown and get the list of teachers
teachers_dropdown = soup.find('select', {'name': 'ctl00$ContentPlaceHolder2$ddlTeacher'})
teachers = teachers_dropdown.find_all('option')[1:]  # Skipping the first option which is the placeholder

# Check if there are no teachers available
if not teachers:
    console.print("[ ✔  ] Teacher evaluation forms already filled", style="bold yellow")
else:
    # Iterate over each teacher and fill out the evaluation form
    for teacher in teachers:
        teacher_value = teacher['value']

        # Select the teacher
        payload = {
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder2$ddlTeacher',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstategenerator,
            '__EVENTVALIDATION': eventvalidation,
            'ctl00$ContentPlaceHolder2$ddlTeacher': teacher_value,
        }

        response = session.post(teacher_evaluation_url, data=payload)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Update hidden form fields after selecting the teacher
        viewstate, eventvalidation, viewstategenerator = update_hidden_fields(soup)

        # Prepare the payload for submitting the teacher evaluation form
        form_payload = {
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstategenerator,
            '__EVENTVALIDATION': eventvalidation,
            'ctl00$ContentPlaceHolder2$q1': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q2': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q3': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q4': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q5': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q6': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q7': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q8': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q9': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q10': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q11': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q12': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q13': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q14': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q15': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q16': 'A',  # Example response
            'ctl00$ContentPlaceHolder2$q20': 'Good instructor',  # Example comment
            'ctl00$ContentPlaceHolder2$q21': 'Good course',  # Example comment
            'ctl00$ContentPlaceHolder2$btnSave': 'Save Proforma Proforma',
        }

        submit_response = session.post(teacher_evaluation_url, data=form_payload)
        print(f"[*] Submitted teacher evaluation for {teacher.text}")

    console.print("[ ✔  ] All teacher evaluations completed.", style="bold green")

# Navigate to the Online Learning Feedback Proforma
response = session.get(online_learning_feedback_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract hidden form fields for the online learning feedback form
viewstate, eventvalidation, viewstategenerator = update_hidden_fields(soup)

# Find the subjects dropdown and get the list of subjects
subjects_dropdown = soup.find('select', {'name': 'ctl00$ContentPlaceHolder1$cmb_courses'})
subjects = subjects_dropdown.find_all('option')[1:]  # Skipping the first option which is the placeholder

# Check if there are no subjects available
if not subjects:
    console.print("[ ✔  ] Online Learning Feedback Proformas already filled", style="bold yellow")
else:
    # Iterate over each subject and fill out the feedback form
    for subject in subjects:
        subject_value = subject['value']

        # Select the subject
        payload = {
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$cmb_courses',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstategenerator,
            '__EVENTVALIDATION': eventvalidation,
            'ctl00$ContentPlaceHolder1$cmb_courses': subject_value,
        }

        response = session.post(online_learning_feedback_url, data=payload)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Update hidden form fields after selecting the subject
        viewstate, eventvalidation, viewstategenerator = update_hidden_fields(soup)

        # Prepare the payload for submitting the feedback form
        form_payload = {
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstategenerator,
            '__EVENTVALIDATION': eventvalidation,
            'ctl00$ContentPlaceHolder1$q1': 'A',  # Example response
            'ctl00$ContentPlaceHolder1$q2': 'A',  # Example response
            'ctl00$ContentPlaceHolder1$q3': 'A',  # Example response
            'ctl00$ContentPlaceHolder1$q4': 'A',  # Example response
            'ctl00$ContentPlaceHolder1$q5': 'A',  # Example response
            'ctl00$ContentPlaceHolder1$q6': 'A',  # Example response
            'ctl00$ContentPlaceHolder1$q7': 'A',  # Example response
            'ctl00$ContentPlaceHolder1$q8': 'A',  # Example response
            'ctl00$ContentPlaceHolder1$q9': 'A',  # Example response
            'ctl00$ContentPlaceHolder1$q10': 'A',  # Example response
            'ctl00$ContentPlaceHolder1$q11': 'A',  # Example response
            'ctl00$ContentPlaceHolder1$q12': 'A',  # Example response
            'ctl00$ContentPlaceHolder1$q13': 'A',  # Example response
            'ctl00$ContentPlaceHolder1$q14': 'A',  # Example response
            'ctl00$ContentPlaceHolder1$q15': 'A',  # Example response
            'ctl00$ContentPlaceHolder1$q20': 'Good online learning experience',  # Example comment
            'ctl00$ContentPlaceHolder1$btnSave': 'Submit Proforma',
        }

        submit_response = session.post(online_learning_feedback_url, data=form_payload)
        print(f"[*] Submitted online learning feedback for subject {subject.text}")

    console.print("[ ✔  ]  All online learning feedback proformas completed.", style="bold green")



# Wait for user input before closing
input("\nPress Enter to close the program...")
