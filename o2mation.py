import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.prompt import Prompt
import getpass
from rich.panel import Panel
from rich.table import Table


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
[bold cyan]Developer GitHub: https://github.com/Aw4iskh4n[/bold cyan]
"""
    console.print(banner_text)

print_banner()
console.print("\n\n\n\n")

# URLs
login_url = "https://portals.au.edu.pk/qec/login.aspx"
base_url = "https://portals.au.edu.pk/qec/"
first_performa_url = base_url + "p1.aspx"
teacher_evaluation_url = base_url + "p10.aspx"
online_learning_feedback_url = base_url + "p10a_learning_online_form.aspx"

def get_password(prompt="Password: "):
    return getpass.getpass(prompt)

def get_login_payload(soup, username, password):
    return {
        'ctl00$ContentPlaceHolder2$ddlcampus': 'Islamabad',
        'ctl00$ContentPlaceHolder2$ddlUserType': 'Student/Alumni',
        'ctl00$ContentPlaceHolder2$txt_regid': username,
        'ctl00$ContentPlaceHolder2$txt_password': password,
        'ctl00$ContentPlaceHolder2$btnAccountlogin': 'Login',
        '__VIEWSTATE':           soup.find('input', {'name': '__VIEWSTATE'})['value'],
        '__EVENTVALIDATION':     soup.find('input', {'name': '__EVENTVALIDATION'})['value'],
        '__VIEWSTATEGENERATOR':  soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value'],
    }

def update_hidden_fields(soup):
    vs  = soup.find('input', {'name': '__VIEWSTATE'})
    ev  = soup.find('input', {'name': '__EVENTVALIDATION'})
    vsg = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})
    return (
        vs['value'] if vs else None,
        ev['value'] if ev else None,
        vsg['value'] if vsg else None,
    )

session = requests.Session()
login_success = False
while not login_success:
    username = Prompt.ask("[bold #f5c816]Enter your ID[/bold #f5c816]")
    password = Prompt.ask("[bold #f5c816]Enter your password: [/bold #f5c816]")
    resp = session.get(login_url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    login_resp = session.post(login_url, data=get_login_payload(soup, username, password))
    if "logout" in login_resp.text.lower():
        console.print("\n[ - ] Login successful\n\n", style="bold green")
        login_success = True
    else:
        console.print("\n[ X ] Login failed. Please try again.\n", style="bold red")

# --- Custom-grade setup ---
resp = session.get(teacher_evaluation_url)
soup = BeautifulSoup(resp.content, 'html.parser')
vs_t, ev_t, vsg_t = update_hidden_fields(soup)

teachers = soup.find('select', {'name': 'ctl00$ContentPlaceHolder2$ddlTeacher'})\
               .find_all('option')[1:]
teacher_list = [(t['value'], t.text.strip()) for t in teachers]

choice = Prompt.ask(
    "\nDo you want to give custom grades? (default 'n')",
    choices=["y", "n"],
    default="n"
)

custom_grades = {}
teacher_course  = {}

# --- Custom-grade setup with Rich panels & tables ---
if choice.lower() == "y":
    # 1) Show a title panel
    console.print(Panel.fit("[bold white]🎓 Custom Grade Assignment 🎓[/bold white]",
                            subtitle="Assign per-teacher grades",
                            style="cyan"))

    # 2) Build and display a table of teachers + (soon) courses
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("No.", justify="center", width=4)
    table.add_column("Teacher", style="bold")
    table.add_column("Course", style="dim")
    for idx, (tv, tn) in enumerate(teacher_list, start=1):
        # placeholder until we fetch course_name
        table.add_row(str(idx), tn, "---")
    console.print(table)

    # 3) Step through each teacher to fetch their course & prompt
    for idx, (tv, tn) in enumerate(teacher_list, start=1):
        # select teacher → load their proforma page
        payload = {
            '__EVENTTARGET':         'ctl00$ContentPlaceHolder2$ddlTeacher',
            '__VIEWSTATE':           vs_t,
            '__VIEWSTATEGENERATOR':  vsg_t,
            '__EVENTVALIDATION':     ev_t,
            'ctl00$ContentPlaceHolder2$ddlTeacher': tv,
        }
        r = session.post(teacher_evaluation_url, data=payload)
        tsoup = BeautifulSoup(r.content, 'html.parser')
        vs_t, ev_t, vsg_t = update_hidden_fields(tsoup)

        # scrape course name more robustly
        elem = tsoup.find(attrs={'id': lambda x: x and 'lblCourse' in x})
        course_name = elem.text.strip() if elem else "Unknown"

        # update the table in-place (optional)
        table.columns[2]._cells[idx-1] = course_name
        console.clear()              # refresh screen
        console.print(Panel.fit("[bold white] Custom Grade Assignment [/bold white]",
                                style="cyan"))
        console.print(table)

        # 4) Prompt:
        prompt_msg = (
            f"[bold yellow]\nGrade for[/bold yellow] "
            f"[bold cyan]{tn}[/bold cyan] "
            f"[bold #f5c816]({course_name})[/bold #f5c816]\n"
            "\nA = Strongly Agree | B = Agree | C = Disagree | D = Strongly Disagree\n\n"
            "Enter the Grade"
        )
        grade = Prompt.ask(prompt_msg,
                           choices=["A","B","C","D"],
                           show_choices=False)
        custom_grades[tv] = grade
        teacher_course[tv] = course_name

    console.print("\n[green][ - ] Custom grades recorded.[/]\n")


# Build subject→grade mapping from Proforma 1
resp = session.get(first_performa_url)
soup = BeautifulSoup(resp.content, 'html.parser')
vs1, ev1, vsg1 = update_hidden_fields(soup)
subjects = soup.find('select', {'name': 'ctl00$ContentPlaceHolder2$cmb_courses'})\
               .find_all('option')[1:]
subject_grade_map = {}
for tv, grade in custom_grades.items():
    course = teacher_course.get(tv)
    if not course:
        continue
    for opt in subjects:
        if opt.text.strip() == course:
            subject_grade_map[opt['value']] = grade
            break

def select_subject_and_submit(session, base_url, subject_value, viewstate, eventvalidation, viewstategenerator, subject, override_grade='A'):
    payload = {
        '__EVENTTARGET': 'ctl00$ContentPlaceHolder2$cmb_courses',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstategenerator,
        '__EVENTVALIDATION': eventvalidation,
        'ctl00$ContentPlaceHolder2$cmb_courses': subject_value,
        **{ f'ctl00$ContentPlaceHolder2$q{i}': override_grade for i in range(1,13) },
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
        console.print(f"      [-] Failed for {subject}", style="bold red")
    return response

# --- Fill Proforma 1 ---
if not subjects:
    console.print("[ - ] Subjects evaluation proforma already filled", style="bold yellow")
else:
    for subject in subjects:
        val = subject['value']
        grade = subject_grade_map.get(val, "A")
        resp = select_subject_and_submit(session, base_url, val, vs1, ev1, vsg1, subject.text, override_grade=grade)
        soup = BeautifulSoup(resp.content, 'html.parser')
        vs1, ev1, vsg1 = update_hidden_fields(soup)
    console.print("[ - ] Subjects evaluation proforma filled successfully.", style="bold green")

# --- Teacher Evaluation Proforma ---
resp = session.get(teacher_evaluation_url)
soup = BeautifulSoup(resp.content, 'html.parser')
vs2, ev2, vsg2 = update_hidden_fields(soup)
teachers = soup.find('select', {'name': 'ctl00$ContentPlaceHolder2$ddlTeacher'})\
               .find_all('option')[1:]

if not teachers:
    console.print("[ - ] Teacher evaluation forms already filled", style="bold yellow")
else:
    for t in teachers:
        tv = t['value']
        tn = t.text.strip()

        # select teacher
        payload = {
            '__EVENTTARGET':         'ctl00$ContentPlaceHolder2$ddlTeacher',
            '__EVENTARGUMENT':       '',
            '__VIEWSTATE':           vs2,
            '__VIEWSTATEGENERATOR':  vsg2,
            '__EVENTVALIDATION':     ev2,
            'ctl00$ContentPlaceHolder2$ddlTeacher': tv,
        }
        r = session.post(teacher_evaluation_url, data=payload)
        tsoup = BeautifulSoup(r.content, 'html.parser')
        vs2, ev2, vsg2 = update_hidden_fields(tsoup)

        grade = custom_grades.get(tv, "A")
        form_payload = {
            '__VIEWSTATE':           vs2,
            '__VIEWSTATEGENATOR':    vsg2,
            '__EVENTVALIDATION':     ev2,
            **{ f'ctl00$ContentPlaceHolder2$q{i}': grade for i in range(1,17) },
            'ctl00$ContentPlaceHolder2$q20': 'Good instructor',
            'ctl00$ContentPlaceHolder2$q21': 'Good course',
            'ctl00$ContentPlaceHolder2$btnSave': 'Save Proforma Proforma',
        }
        session.post(teacher_evaluation_url, data=form_payload)
        console.print(f"      [-] Submitted for {tn} (Grade: {grade})", style="bold #8a8a8a")

    console.print("[ - ] Teacher evaluations proforma filled successfully.", style="bold green")

# --- Online Learning Feedback Proforma ---
resp = session.get(online_learning_feedback_url)
soup = BeautifulSoup(resp.content, 'html.parser')
vs3, ev3, vsg3 = update_hidden_fields(soup)
subjects = soup.find('select', {'name': 'ctl00$ContentPlaceHolder1$cmb_courses'})\
               .find_all('option')[1:]

if not subjects:
    console.print("[ - ] Online Learning Feedback Proformas already filled", style="bold yellow")
else:
    for subject in subjects:
        sv = subject['value']
        payload = {
            '__EVENTTARGET':         'ctl00$ContentPlaceHolder1$cmb_courses',
            '__EVENTARGUMENT':       '',
            '__VIEWSTATE':           vs3,
            '__VIEWSTATEGENERATOR':  vsg3,
            '__EVENTVALIDATION':     ev3,
            'ctl00$ContentPlaceHolder1$cmb_courses': sv,
        }
        r = session.post(online_learning_feedback_url, data=payload)
        osoup = BeautifulSoup(r.content, 'html.parser')
        vs3, ev3, vsg3 = update_hidden_fields(osoup)

        grade = subject_grade_map.get(sv, "A")
        form_payload = {
            '__VIEWSTATE':           vs3,
            '__VIEWSTATEGENERATOR':  vsg3,
            '__EVENTVALIDATION':     ev3,
            **{ f'ctl00$ContentPlaceHolder1$q{i}': grade for i in range(1,16) },
            'ctl00$ContentPlaceHolder1$q20': 'Good online learning experience',
            'ctl00$ContentPlaceHolder1$btnSave': 'Submit Proforma',
        }
        session.post(online_learning_feedback_url, data=form_payload)
        console.print(f"      [-] Submitted for {subject.text}", style="bold #8a8a8a")

    console.print("[-] Online learning feedback proformas filled successfully.\n\n", style="bold green")

input("\nPress Enter to close the program...")
