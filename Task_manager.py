## Task Manager
## Author: Fabian Ciriani
## Date: 2022-04-26

print("Task Manager")

## IMPORTS

import json
import smtplib
from email.message import EmailMessage
from datetime import datetime
from Test_mail import enviar_email
from daily_reminder import daily_reminder
import threading
import sys
import os
from dotenv import load_dotenv  ## pip install python-dotenv
import time
import schedule

print("Python en uso:", sys.executable)

## GLOBAL VARIABLES

tasks = []  ## a list of dictionaries, one for each task
finished_tasks = [] ## a list of dictionaries, one for each finished task

load_dotenv(dotenv_path="User_info.env")

user = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")
user_ing = os.getenv("EMAIL_ING")
user_flor = os.getenv("EMAIL_FLOR")
destinatary_selection = {
    "1": (user_ing, "Ingenieria Giannini"),
    "2": (user, "Fabi"),
    "3": (user_flor, "Flor")}

destinatario = destinatary_selection["2"][0]

### TASK FUNCTIONS

def gets_tasks():
    print("Tareas pendientes:")

    # ordenar por fecha y hora
    tasks.sort( key=lambda t: datetime.strptime(
            t["date"] + " " + t["hour"], "%d/%m/%Y %H:%M"
        )
    )

    for i, t in enumerate(tasks, start=1):
        print("\n")
        print("Tarea Nro:", i)
        print(
            " Tarea:", t["description"], "\n",
           
            "Fecha:", t["date"], "\n",
            "Hora:", t["hour"], "\n",
            "Hora creada:", t["hour_created"], "\n",
            "Fecha creada:", t["date_created"]
        )
    
    return tasks
        


def add_task():
## add a task to the list
    description = input("Descripción: ") ## user input description of the task

    while True:

       date_of_task = input("Fecha (dd/mm/aaaa): ") ## user input date of the task
       try:
           datetime.strptime(date_of_task, "%d/%m/%Y")
           break
       
       except ValueError:
           print("Formato de fecha incorrecto, ingrese nuevamente")

    while True:  
       hour_of_task = input("Hora (hh:mm): ") ## user input hour of the task
       try:
           datetime.strptime(hour_of_task, "%H:%M")
           break
       
       except ValueError:
           print("Formato de hora incorrecto, ingrese nuevamente")
        
    hour_created = datetime.now().strftime("%H:%M") ## get the current hour
    date_created = datetime.now().strftime("%d/%m/%Y") ## get the current date 
    my_task = {
        "description": description,
        "date": date_of_task,
        "hour": hour_of_task,
        "hour_created": hour_created,
        "date_created": date_created,
        "finished": False
    }
    tasks.append(my_task)
    save_tasks()

def finish_task():
## mark a task as finished
    global finished_tasks
    task_number = input("Seleccione la tarea a marcar como finalizada (nro): ") ## user select the task to mark as finished
    description = tasks[int(task_number) - 1]["description"]
    for t in tasks:
        if t["description"] == description:
            t["finished"] = True
            finished_tasks.append(t)
            tasks.remove(t)
            save_tasks()
            print("Tarea finalizada")



## FILE FUNCTIONS

def save_tasks():
## save the list of tasks to a file in JSON format, for future use and not loosing data
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)


def load_tasks():
## load the list of tasks from a file in JSON format, when the program starts
    global tasks
    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    except:
        tasks = []

    return tasks    

## EMAIL FUNCTIONS

def send_email(a_list_of_tasks, subject, usuario, clave, destinatario):

    print("Sending email...")
    enviar_email(a_list_of_tasks, subject, usuario, clave, destinatario)

## MAIN FUNCTION

def main():
    threading.Thread(
        target=daily_reminder,
        args=(send_email, tasks, "Recordatorio de tareas pendientes", user , password , destinatario ),
        daemon=True
    ).start()
    while True: 
    
       print("Task Manager")
       print ("1. Mostrar tareas")
       print ("2. Agregar tarea")
       print ("3. Marcar tarea como finalizada")
       print ("4. Enviar correo")
       print ("5. Salir")

       option = input("Opcion: ")
       if option == "1":
           gets_tasks()
       elif option == "2":
           add_task()
       elif option == "3":
           finish_task()
       elif option == "4":
           print("Seleccione destinatario: 1: Giannini, 2: Fabi, 3: Flor ")
           option = input("Opcion: ")
           destinatary = destinatary_selection[option][0]
           send_email(tasks, "Recordatorio de tareas pendientes", user, password, destinatary)
       elif option == "5":
           print("Gracias por usar Task Manager")
           exit()
       else:
           print("Opcion no valida")
        

if __name__ == "__main__":
    load_tasks()
    main()