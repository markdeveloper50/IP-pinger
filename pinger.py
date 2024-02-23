import subprocess
import tkinter as tk
from tkinter import Label, Button, messagebox
import threading
import re

# Add IP addresses and hostnames to be pinged along with their labels
data = [
    {'ip': '8.8.8.8', 'hostname': 'Google'}, 
]
def ping_ip(ip, label, rt_label):
    try:
        # Run the ping command
        result = subprocess.run(['ping', '-n', '1', ip], capture_output=True, text=True, timeout=5)
        match = re.search(r"time=(\d+)ms", result.stdout)
        if match:
            round_trip_time_str = match.group(1) + "ms"  
        else:
            round_trip_time_str = 'Round-trip time not found in the output.'
        # Extract time information
        if result.returncode == 0:
            label.config(bg='green',foreground='white')  # Set label background to green for online
        else:
            label.config(bg='red',foreground='white')    # Set label background to red for offline
    except subprocess.TimeoutExpired:
        round_trip_time_str = 'Timeout'
        label.config(bg='yellow')     # Set label background to yellow for timeout
    # Update round-trip time label
    rt_label.config(text=f"Time: {round_trip_time_str}")

def tracert_ip(ip):
    try:
        # Run the tracert command
        result = subprocess.run(['tracert', '-d', ip], capture_output=True, text=True, timeout=90)
        tracert_output = result.stdout
        # Show the tracert output in a message box
        messagebox.showinfo("Tracert Output", tracert_output)
    except subprocess.TimeoutExpired:
        messagebox.showerror("Error", "Tracert operation timed out.")

def ping_ips():
    for entry in data:
        ip = entry['ip']
        label = entry['label']
        rt_label = entry['rt_label']
        threading.Thread(target=ping_ip, args=(ip, label, rt_label)).start()
    root.after(1000, ping_ips)  # Repeat every 1000 milliseconds (1 second)

# Create the main window
root = tk.Tk()
root.title("Server Status Report - Powered by TechClone")

# Create a list to store labels and round-trip time labels
labels = []

# Create a label for each IP and arrange them into rows
for i, entry in enumerate(data, start=1):
    hostname = entry['hostname']
    ip = entry['ip']
    label = Label(root, text=f"{hostname} ({ip})", width=25, height=3)
    label.grid(row=i, column=0, padx=5, pady=5)  # Grid layout
    rt_label = Label(root, text="Time: ", width=40, height=3)
    rt_label.grid(row=i, column=1, padx=5, pady=5)  # Grid layout
    labels.append(label)
    entry['label'] = label
    entry['rt_label'] = rt_label
    tracert_button = Button(root, text="Tracert", command=lambda ip=ip: tracert_ip(ip))
    tracert_button.grid(row=i, column=2, padx=5, pady=5)  # Grid layout

# Start pinging IPs automatically
ping_ips()

# Run the Tkinter event loop
root.mainloop()
