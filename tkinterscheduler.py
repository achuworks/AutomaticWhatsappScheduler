import pyautogui as auto
import time
from datetime import datetime
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog
import threading

# Global list to store tasks
tasks = []

def schedule_whatsapp_message(task):
    """Send the WhatsApp message with optional file attachment."""
    try:
        webbrowser.open('https://web.whatsapp.com')
        time.sleep(15)  # Allow time for WhatsApp Web to load
        auto.press('esc')
        auto.press('enter')
        auto.moveTo(200, 100)
        auto.click()
        time.sleep(1)
        auto.moveTo(374, 248)
        auto.click()
        time.sleep(1)

        auto.write(task["group_name"])
        for receiver in task["recipients"]:
            temp = task["message"] + " " + receiver
            time.sleep(1)
            auto.press('enter')
            time.sleep(1)
            auto.write(temp)
            auto.press('enter')
            time.sleep(1)

            # Attach file if provided
            if task["file_path"]:
                auto.click(x=708, y=953)  # Click on the attachment icon (adjust coordinates as needed)
                time.sleep(1)
                auto.click(x=813, y=573)  # Select file option
                time.sleep(1)
                auto.write(task["file_path"])
                auto.press('enter')
                time.sleep(2)
                auto.press('enter')  # Send the file
                time.sleep(1)

        task["status"] = "Completed"
    except Exception as e:
        task["status"] = f"Error: {str(e)}"
    finally:
        update_task_list_ui()

def task_scheduler():
    """Check for tasks to execute."""
    while True:
        now = datetime.now()
        for task in tasks:
            if task["status"] == "Pending" and now >= task["date_time"]:
                task["status"] = "In Progress"
                update_task_list_ui()
                schedule_whatsapp_message(task)
        time.sleep(1)

def add_task():
    """Add a new task to the list."""
    group_name = group_name_var.get()
    recipients = recipient_var.get().split(",")
    message = message_var.get()
    date_time = datetime.strptime(date_time_var.get(), "%Y-%m-%d %H:%M")
    file_path = file_path_var.get()
    
    # Add task to the global list
    task = {
        "group_name": group_name,
        "recipients": recipients,
        "message": message,
        "date_time": date_time,
        "file_path": file_path,
        "status": "Pending"
    }
    tasks.append(task)
    update_task_list_ui()

def browse_file():
    """Open a file dialog to select a file."""
    file_path = filedialog.askopenfilename()
    file_path_var.set(file_path)

def update_task_list_ui():
    """Update the task list in the UI."""
    task_list.delete(*task_list.get_children())  # Clear the list
    for idx, task in enumerate(tasks):
        task_list.insert("", "end", values=(idx + 1, task["group_name"], ", ".join(task["recipients"]),
                                            task["message"], task["date_time"].strftime("%Y-%m-%d %H:%M"),
                                            task["status"], task["file_path"]))

# UI Setup
root = tk.Tk()
root.title("WhatsApp Message Scheduler with File Attachments")

# Input Fields
tk.Label(root, text="Group Name:").grid(row=0, column=0, padx=10, pady=5)
group_name_var = tk.StringVar()
tk.Entry(root, textvariable=group_name_var).grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Recipients (comma-separated):").grid(row=1, column=0, padx=10, pady=5)
recipient_var = tk.StringVar()
tk.Entry(root, textvariable=recipient_var).grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Message:").grid(row=2, column=0, padx=10, pady=5)
message_var = tk.StringVar()
tk.Entry(root, textvariable=message_var).grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Date and Time (YYYY-MM-DD HH:MM):").grid(row=3, column=0, padx=10, pady=5)
date_time_var = tk.StringVar()
tk.Entry(root, textvariable=date_time_var).grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Browse and select the file name(dont give the path):").grid(row=4, column=0, padx=10, pady=5)
file_path_var = tk.StringVar()
tk.Entry(root, textvariable=file_path_var).grid(row=4, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_file).grid(row=4, column=2, padx=5, pady=5)

tk.Button(root, text="Add Schedule", command=add_task).grid(row=5, column=0, columnspan=3, pady=10)

# Task List Display
columns = ("ID", "Group Name", "Recipients", "Message", "Date & Time", "Status", "File Path")
task_list = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    task_list.heading(col, text=col)
    task_list.column(col, width=150)
task_list.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

# Start the task scheduler thread
scheduler_thread = threading.Thread(target=task_scheduler, daemon=True)
scheduler_thread.start()

root.mainloop()