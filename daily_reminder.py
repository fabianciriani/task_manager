## daily reminder

import time
from datetime import datetime , date
import json
import os

def daily_reminder(mail_function, tasks_list, subject, user, password, destinatary):

    
    try:        

      with open("last_sent_day.json", "r") as file:        
         data = json.load(file)["last_day"]
    
    except (FileNotFoundError, json.JSONDecodeError):

        initday = str(date(2000, 1, 1))
        with open("last_sent_day.json", "w") as file:
            json.dump({"last_day": initday}, file, indent=4)
        
        with open("last_sent_day.json", "r") as file:
            data = json.load(file)["last_day"] 

    last_sent_day = date.fromisoformat(data) 

    while True:
        now = datetime.now()
        reminder_hour = 7

        if now.hour >= reminder_hour and last_sent_day != now.date():
            print("Recordatorio de tareas pendientes")

            try:
                mail_function(tasks_list, subject, user, password, destinatary)
                last_sent_day = now.date()

            except Exception as e:
                print("Error al enviar el correo:", e)    
            
            with open("last_sent_day.json", "w") as file:
                json.dump({"last_day": str(last_sent_day)}, file, indent=4)
            
        time.sleep(60)

print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
print(datetime.now().date())
print(date(1999, 1, 1  ))