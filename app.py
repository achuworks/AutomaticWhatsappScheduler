import pyautogui as auto
import time
from datetime import datetime
import webbrowser
import mysql.connector


connection=mysql.connector.connect(
    
    host="localhost",
    user="root",
    password="",
    database="whatsapp_db"
)
cursor=connection.cursor()
cursor.execute("SELECT name,date_of_birth,time from data_of_birth where MONTH(date_of_birth)=MONTH(CURDATE()) AND DAY(date_of_birth)=DAY(CURDATE())")
rows=cursor.fetchall()



def schedule_whatsapp_message(groupName,rows):
    
    webbrowser.open('https://web.whatsapp.com')
    time.sleep(10) 
    auto.press('esc')
    time.sleep(1) 
    auto.press('tab')
    time.sleep(1)
    auto.write(groupName)
    auto.press('enter')
    time.sleep(3)
    auto.moveTo(185, 181)  
    auto.click()
    time.sleep(1)
    auto.write(groupName)
    auto.press('enter')
    auto.moveTo(728,929)
    auto.click()
    
    
    
    

    receivers = [row[0] for row in rows]
    message="Happy Birthday " 
    
    for i  in receivers:
        temp=message+i
        time.sleep(1)
        auto.press('enter')
        time.sleep(3)
        auto.write(temp)
        auto.press('enter')
        time.sleep(2)
        
       

current_time = datetime.now().strftime("%H:%M")
groupName="HOD Subasree Mam"

schedule_whatsapp_message(groupName,rows)
time.sleep(2)

auto.hotkey('alt', 'f4')