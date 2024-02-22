import subprocess
import tkinter as tk
from tkinter import scrolledtext
import threading
import re

# Add comma seprated IP's to be pinged in this array 
data = ['8.8.8.8']

def ping_ip(ip, text_widget):
    try:
        # Run the ping command
        result = subprocess.run(['ping', '-n', '1', ip], capture_output=True, text=True, timeout=5)
        match = re.search(r"time=(\d+)ms", result.stdout)
        if match:
            round_trip_time_str = match.group(0)  
        else:
            round_trip_time_str = 'Round-trip time not found in the output.'
        # Extract time information
        if result.returncode == 0:
            response_data = f"IP: {ip}\n{round_trip_time_str}\n"
            response_status = 'Status: Online\n'
            text_widget.tag_config('status_tag', foreground='green')
        else:
            response_data = f"IP: {ip}\n{result.stderr}\n"
            response_status = 'Status: Offline\n'
            text_widget.tag_config('status_tag', foreground='red')

    except subprocess.TimeoutExpired:
        response_data = f"IP: {ip}\nStatus: Timeout\n"

    # Update the text widget with the formatted data
    text_widget.delete('1.0', tk.END)
    text_widget.insert(tk.END, response_data)
    text_widget.insert(tk.END, response_status, 'status_tag')
    text_widget.yview(tk.END)  # Auto-scroll to the end

def ping_ips():
    for ip, text_widget in zip(data, text_widgets):
        threading.Thread(target=ping_ip, args=(ip, text_widget)).start()
    root.after(1000, ping_ips)  # Repeat every 1000 milliseconds (1 seconds)

# Create the main window
root = tk.Tk()
root.title("Server Status Report - Powered by Smile :)")

# Create a list to store text widgets
text_widgets = []

# Create a text widget for each IP and arrange them into rows of three
for i, ip in enumerate(data, start=1):
    ip_text = scrolledtext.ScrolledText(root, width=50, height=6)
    ip_text.grid(row=(i-1)//2, column=(i-1)%2, padx=5, pady=5)  # Grid layout
    text_widgets.append(ip_text)

# Start pinging IPs automatically
ping_ips()

# Run the Tkinter event loop
root.mainloop()
