### Check tasks

import time
import schedule
import json
import smtplib
from Test_mail import enviar_email
from datetime import datetime


def check_tasks(user, password, destinatario):
    now = datetime.now()
    nowhour = datetime.strptime(now.strftime("%H:%M"), "%H:%M")
    with open("tasks.json", "r") as file:
        tasks = json.load(file)

    for t in tasks:
        task_hour = datetime.strptime(t["hour"], "%H:%M")
        task_day = str(datetime.strptime(t["date"], "%d/%m/%Y").date())

        if abs(task_hour - nowhour).total_seconds() < 60 and task_day == now.strftime("%d/%m/%Y"):
            enviar_email(t, "Recordatorio de tareas pendientes", user, password, destinatario)

now = datetime.now()
print(now)
print(type(now))
nowhour = datetime.strptime(now.strftime("%H:%M"), "%H:%M")
print(nowhour)
print(type(nowhour))