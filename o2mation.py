import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.prompt import Prompt
import sys
import msvcrt

console = Console()

def print_banner():
    banner_text = """


[bold #0c7ec9] ██████╗ ███████╗ ██████╗     ██████╗ ██████╗ ███╗   ███╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
██╔═══██╗██╔════╝██╔════╝    ██╔═══██╗╚════██╗████╗ ████║██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
██║   ██║█████╗  ██║         ██║   ██║ █████╔╝██╔████╔██║███████║   ██║   ██║██║   ██║██╔██╗ ██║
[bold #bf06bf]██║▄▄ ██║██╔══╝  ██║         ██║   ██║██╔═══╝ ██║╚██╔╝██║██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
╚██████╔╝███████╗╚██████╗    ╚██████╔╝███████╗██║ ╚═╝ ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
 ╚══▀▀═╝ ╚══════╝ ╚═════╝     ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                                                                

[/]
[bold #c71482]Developer Instagram: https://instagram.com/_mohmdawais[/bold #c71482]
[bold cyan]Developer GitHub: https://github.com/Aw4iskh4n[/bold cyan]
    """
    console.print(banner_text)

print_banner()

console.print("Developer Instagram: [bold magenta]_mohmdawais\n\n\n\n")

# Define the URLs
login_url = "https://portals.au.edu.pk/qec/login.aspx"
base_url = "https://portals.au.edu.pk/qec/"
first_performa_url = base_url + "p1.aspx"
teacher_evaluation_url = base_url + "p10.aspx"
online_learning_feedback_url = base_url + "p10a_learning_online_form.aspx"

def get_password(prompt="Password: "):
    """Prompt for password with masking."""
    password = ""
    console.print(prompt, end="", style="bold yellow")
    sys.stdout.flush()
    while True:
        ch = msvcrt.getch()
        if ch in {b'\r', b'\n'}:
            print('')
            break
        elif ch == b'\x08':  # Handle backspace
            if len(password) > 0:
                password = password[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        else:
            password += ch.decode('utf-8')
            sys.stdout.write('*')
            sys.stdout.flush()
    return password



def get_login_payload(soup, username, password):
    return {
        'ctl00$ContentPlaceHolder2$ddlcampus': 'Islamabad',
        'ctl00$ContentPlaceHolder2$ddlUserType': 'Student/Alumni',
        'ctl00$ContentPlaceHolder2$txt_regid': username,
        'ctl00$ContentPlaceHolder2$txt_password': password,
        'ctl00$ContentPlaceHolder2$btnAccountlogin': 'Login',
        '__VIEWSTATE': soup.find('input', {'name': '__VIEWSTATE'})['value'],
        '__EVENTVALIDATION': soup.find('input', {'name': '__EVENTVALIDATION'})['value'],
        '__VIEWSTATEGENERATOR': soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
    }

session = requests.Session()

login_success = False
while not login_success:
    username = Prompt.ask("[bold #f5c816]Enter your ID[/bold #f5c816]")
    password = get_password("[bold #f5c816]Enter your password: [/bold #f5c816]")
    response = session.get(login_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    login_response = session.post(login_url, data=get_login_payload(soup, username, password))

    if "logout" in login_response.text.lower():
        console.print("\n[ - ] Login successful\n\n", style="bold green")
        login_success = True
    else:
        console.print("\n[ X ] Login failed. Please try again.\n", style="bold red")
# Function to update hidden fields
def update_hidden_fields(soup):
    """
    Extract hidden fields from the page, returning None for missing fields.
    """
    try:
        viewstate = soup.find('input', {'name': '__VIEWSTATE'})
        eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})
        viewstategenerator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})

        return (
            viewstate['value'] if viewstate else None,
            eventvalidation['value'] if eventvalidation else None,
            viewstategenerator['value'] if viewstategenerator else None,
        )
    except Exception as e:
        console.print(f"[ - ] Error extracting hidden fields: {e}", style="bold red")
        return None, None, None

def select_subject_and_submit(session, base_url, subject_value, viewstate, eventvalidation, viewstategenerator,subject):
    """
    Select a subject and submit the form.
    """
    payload = {
        '__EVENTTARGET': 'ctl00$ContentPlaceHolder2$cmb_courses',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstategenerator,
        '__EVENTVALIDATION': eventvalidation,
        'ctl00$ContentPlaceHolder2$cmb_courses': subject_value,
        'ctl00$ContentPlaceHolder2$q1': 'A',  # Example response
        'ctl00$ContentPlaceHolder2$q2': 'A',
        'ctl00$ContentPlaceHolder2$q3': 'A',
        'ctl00$ContentPlaceHolder2$q4': 'A',
        'ctl00$ContentPlaceHolder2$q5': 'A',
        'ctl00$ContentPlaceHolder2$q6': 'A',
        'ctl00$ContentPlaceHolder2$q7': 'A',
        'ctl00$ContentPlaceHolder2$q8': 'A',
        'ctl00$ContentPlaceHolder2$q9': 'A',
        'ctl00$ContentPlaceHolder2$q10': 'A',
        'ctl00$ContentPlaceHolder2$q11': 'A',
        'ctl00$ContentPlaceHolder2$q12': 'A',
        'ctl00$ContentPlaceHolder2$btnSave': 'Submit Proforma',
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': base_url + 'p1.aspx',
    }

    response = session.post(base_url + 'p1.aspx', data=payload, headers=headers)
    if "successfully" in response.text.lower():
        console.print(f"      [-] Submitted for {subject}", style="bold #8a8a8a")
    else:
        console.print(f"      [-] Failed to submit for {subject}", style="red")
    
    return response

# Get first performa page
performa_page = session.get(first_performa_url)
performa_soup = BeautifulSoup(performa_page.content, 'html.parser')
viewstate, eventvalidation, viewstategenerator = update_hidden_fields(performa_soup)

# Get subjects
subjects_dropdown = performa_soup.find('select', {'name': 'ctl00$ContentPlaceHolder2$cmb_courses'})
subjects = subjects_dropdown.find_all('option')[1:]  # Skip the placeholder

if not subjects:
    console.print("[ - ] Subjects evaluation  proforma already filled", style="bold yellow")
else:
    for subject in subjects:
        subject_value = subject['value']
        # console.print(f"[-] Processing subject: {subject.text}", style=" ")

        response = select_subject_and_submit(
            session, base_url, subject_value, viewstate, eventvalidation, viewstategenerator,subject.text
        )

        # Update hidden fields for subsequent requests
        soup = BeautifulSoup(response.content, 'html.parser')
        viewstate, eventvalidation, viewstategenerator = update_hidden_fields(soup)

    console.print("[ - ] Subjects evaluation proforma filled Successfully.\n", style="green")


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
    console.print("[ - ] Teacher evaluation forms already filled", style="bold yellow")
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

        # Update hidden fields after selecting the teacher
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
        console.print(f"      [-] Submitted for {teacher.text}", style="bold #8a8a8a")

    console.print("[ - ] Teacher evaluations proforma filled successfuly.\n", style="bold green")

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
    console.print("[ - ] Online Learning Feedback Proformas already filled", style="bold yellow")
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

        # Update hidden fields after selecting the subject
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
        console.print(f"      [-] Submitted for {subject.text}", style="bold #8a8a8a")

    console.print("[-] Online learning feedback proformas filled successfully.\n\n", style="bold green")

# Wait for user input before closing
input("\nPress Enter to close the program...")
