import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from datetime import datetime, timedelta
import os

recipients = ["Aakriti.Razdan@helixr.com", "Phani.Sabnivisu@helixr.com"]
sender = "Seyaan.Budhkar@helixr.com"

def get_tasks(country, month, day):
    conn = sqlite3.connect("database/final_database.db")
    cursor = conn.cursor()
    
    cursor.execute(f'''
    select TaskName
    from tasks_{country}, events_{country}
    where tasks_{country}.TaskID == events_{country}.TaskID
    and Month = {month}
    and Day = {day}
    ''')

    tasks = cursor.fetchall()

    conn.close()

    return tasks


def create_message():

    advance_date = datetime.now() + timedelta(days=3)
    month = advance_date.month
    day = advance_date.day

    uk_tasks = get_tasks("uk", month, day)
    ir_tasks = get_tasks("ir", month, day)
    in_tasks = get_tasks("in", month, day)
    fi_tasks = get_tasks("fi", month, day)
    
    message = "Hi, \n\nThis is a reminder that the following tasks are due in 3 days:\n\n"
        
    if len(uk_tasks) > 0:
        message += "UK: \n"
        for task in uk_tasks:
            message += f"- {task[0]}\n"
        message += "\n"

    if len(ir_tasks) > 0:
        message += "Ireland: \n"
        for task in ir_tasks:
            message += f"- {task[0]}\n"
        message += "\n"
        
    if len(in_tasks) > 0:
        message += "India: \n"
        for task in in_tasks:
            message += f"- {task[0]}\n"
        message += "\n"
        
    if len(fi_tasks) > 0:
        message += "Finance Team: \n"
        for task in fi_tasks:
            message += f"- {task[0]}\n"
        message += "\n"

    return message

def send_email(message):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['Subject'] = "Task Reminder"
    msg.attach(MIMEText(message, 'plain'))

    smtp_password = os.getenv("SENDGRID_API_KEY")

    server = smtplib.SMTP("smtp.sendgrid.net", 25)
    server.starttls()
    server.login("apikey", smtp_password)

    text = msg.as_string()
    for recipient in recipients:
        msg['To'] = recipient
        server.sendmail(sender, recipient, text)
    server.quit()

if __name__ == '__main__':
    advance_date = datetime.now() + timedelta(days=3)
    month = advance_date.month
    day = advance_date.day

    task_list1 = len(get_tasks("uk", month, day))
    task_list2 = len(get_tasks("ir", month, day))
    task_list3 = len(get_tasks("in", month, day))
    task_list4 = len(get_tasks("fi", month, day))

    if (task_list1 + task_list2 + task_list3 + task_list4) > 0:
        message = create_message()
        send_email(message)    
    