## test send email

import smtplib
from email.mime.text import MIMEText
import time
from datetime import datetime , date
import os



def enviar_email(a_list_of_tasks, subject, user, password, destinatary):
    remitente =user
    contraseña = password
    destinatario = destinatary
    passed_tasks = []
    today_tasks = []
    next_tasks = []

    today = datetime.now().date()

    for task in a_list_of_tasks:
       
       task_date = datetime.strptime(task["date"],"%d/%m/%Y").date()

       if task_date < today:
           passed_tasks.append(task)

       elif task_date == today:
           today_tasks.append(task)

       elif task_date > today:
           next_tasks.append(task)    

    my_message = "Recordatorio de tareas pendientes: \n\n"

    if not a_list_of_tasks:

        my_message += "No hay tareas pendientes"

    if not passed_tasks:

        my_message += "No hay tareas vencidas\n\n"    

    if not today_tasks:

        my_message += "No hay tareas el dia de hoy\n\n"     

    if not next_tasks:

        my_message += "No hay tareas proximamente\n\n"        

    for task in passed_tasks:
             
        my_message += "Tareas pasadas / vencidas: \n\n"
        my_message += f"Descripción: {task['description']}\n"
        my_message += f"Fecha: {task['date']}\n"
        my_message += f"Hora: {task['hour']}\n\n"

    for task in today_tasks:

        my_message += "Tareas del dia: \n\n"
        my_message += f"Descripción: {task['description']}\n"
        my_message += f"Fecha: {task['date']}\n"
        my_message += f"Hora: {task['hour']}\n\n"

    for task in next_tasks:   

        my_message += "Tareas proximas: \n\n"
        my_message += f"Descripción: {task['description']}\n"
        my_message += f"Fecha: {task['date']}\n"
        my_message += f"Hora: {task['hour']}\n\n"     

    mensaje = MIMEText(my_message)
    mensaje["Subject"] = subject
    mensaje["From"] = remitente
    mensaje["To"] = destinatario

    print(remitente, destinatario)

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remitente, contraseña)

        servidor.send_message(mensaje)
        servidor.quit()

        print("✅ Email enviado correctamente")

    except Exception as e:
        print("❌ Error:", e)

"""
if __name__ == "__main__":
    enviar_email(a_list_of_tasks)
"""

