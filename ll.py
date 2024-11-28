import tkinter as tk
import pyautogui

def update_position():
    # Get the mouse cursor position
    x, y = pyautogui.position()
    
    # Update the label with the current position
    position_label.config(text=f"X: {x}, Y: {y}")
    
    # Call the function again after 100 milliseconds
    window.after(100, update_position)

window = tk.Tk()
window.title("Mouse Position Tracker")

# Create a label to display the mouse coordinates
position_label = tk.Label(window, font=("Arial", 14))
position_label.pack(padx=10, pady=10)

# Start the update function
update_position()

# Run the GUI main loop
window.mainloop()