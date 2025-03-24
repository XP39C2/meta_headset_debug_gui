import tkinter as tk
import subprocess
import os
from datetime import datetime

def run_adb_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        result = f"Error executing command:\n{e.output}"
    return result

def get_connected_devices():
    output = run_adb_command("adb devices")
    devices = []
    lines = output.strip().splitlines()
    for line in lines[1:]:
        if line.strip():
            parts = line.split()
            if parts:
                devices.append(parts[0])
    return devices

def update_dropdown(devices):
    menu = device_dropdown["menu"]
    menu.delete(0, "end")
    if devices:
        for device in devices:
            menu.add_command(label=device, command=lambda d=device: selected_device.set(d))
        selected_device.set(devices[0])
    else:
        selected_device.set("No devices")
        menu.add_command(label="No devices", command=lambda: None)

def update_battery_label():
    battery_output = run_adb_command("adb shell dumpsys battery")
    level, scale = None, None
    for line in battery_output.splitlines():
        line = line.strip()
        if line.startswith("level:"):
            try:
                level = int(line.split(":", 1)[1].strip())
            except ValueError:
                pass
        elif line.startswith("scale:"):
            try:
                scale = int(line.split(":", 1)[1].strip())
            except ValueError:
                pass
    if level is not None and scale is not None and scale != 0:
        battery_percentage = level * 100 // scale
        battery_label.config(text=f"Battery: {battery_percentage}%")
    else:
        battery_label.config(text="Battery: N/A")

def update_status():
    output = run_adb_command("adb devices")
    display_output(f"Device Status:\n{output}")
    devices = get_connected_devices()
    update_dropdown(devices)
    update_battery_label()

def reboot_headset():
    device = selected_device.get()
    if device == "No devices":
        display_output("No device selected.")
        return
    output = run_adb_command(f"adb -s {device} reboot")
    display_output(f"Reboot Command Output:\n{output}")
    update_battery_label()

def launch_scrcpy():
    scrcpy_path = r"C:\scrcpy-win64-v3.1\scrcpy-win64-v3.1\scrcpy.exe"
    device = selected_device.get()
    command = f'"{scrcpy_path}"'
    if device != "No devices":
        command += f" -s {device}"
    try:
        subprocess.Popen(command, shell=True)
        display_output("Launching scrcpy...")
    except Exception as e:
        display_output(f"Error launching scrcpy:\n{e}")

def display_logs():
    output = run_adb_command("adb logcat -d")
    display_output(f"Logs:\n{output}")

def open_adb_shell():
    try:
        subprocess.Popen('start cmd /k "adb shell"', shell=True)
        display_output("Opened ADB shell in a new command prompt.")
    except Exception as e:
        display_output(f"Error opening ADB shell: {e}")

def run_predefined_command(command):
    device = selected_device.get()
    if device != "No devices":
        command = command.replace("adb", f"adb -s {device}", 1)
    output = run_adb_command(command)
    display_output(f"Output for '{command}':\n{output}")

def save_output_to_desktop():
    text = status_text.get(1.0, tk.END)
    if not text.strip():
        display_output("Nothing to save.")
        return
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(desktop, f"adb_output_{timestamp}.txt")
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        display_output(f"Output saved to {filename}")
    except Exception as e:
        display_output(f"Error saving output: {e}")

def wake_device():
    output = run_adb_command("adb shell input keyevent KEYCODE_WAKEUP")
    display_output("Waking up device...\n" + output)

def display_output(text):
    status_text.config(state=tk.NORMAL)
    status_text.delete(1.0, tk.END)
    status_text.insert(tk.END, text)
    status_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Meta Quest ADB Troubleshooter")
root.geometry("1000x600")

top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

update_button = tk.Button(top_frame, text="Update Status", command=update_status)
update_button.pack(side=tk.LEFT, padx=5)

reboot_button = tk.Button(top_frame, text="Reboot Headset", command=reboot_headset)
reboot_button.pack(side=tk.LEFT, padx=5)

scrcpy_button = tk.Button(top_frame, text="Launch scrcpy", command=launch_scrcpy)
scrcpy_button.pack(side=tk.LEFT, padx=5)

logs_button = tk.Button(top_frame, text="Display Logs", command=display_logs)
logs_button.pack(side=tk.LEFT, padx=5)

adb_shell_button = tk.Button(top_frame, text="Open ADB Shell", command=open_adb_shell)
adb_shell_button.pack(side=tk.LEFT, padx=5)

selected_device = tk.StringVar()
selected_device.set("No devices")
device_dropdown = tk.OptionMenu(top_frame, selected_device, "No devices")
device_dropdown.pack(side=tk.LEFT, padx=5)

hardware_commands = {
    "Properties": "adb shell getprop",
    "Battery": "adb shell dumpsys battery",
    "Sensors": "adb shell dumpsys sensorservice",
    "Camera": "adb shell dumpsys media.camera",
    "Display": "adb shell dumpsys display"
}

hardware_btn = tk.Menubutton(top_frame, text="Hardware Check", relief=tk.RAISED)
hardware_menu = tk.Menu(hardware_btn, tearoff=0)
hardware_btn.config(menu=hardware_menu)
for friendly_name, command in hardware_commands.items():
    hardware_menu.add_command(label=friendly_name, command=lambda c=command: run_predefined_command(c))
hardware_btn.pack(side=tk.LEFT, padx=5)

battery_label = tk.Label(top_frame, text="Battery: N/A")
battery_label.pack(side=tk.LEFT, padx=5)

output_frame = tk.Frame(root)
output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

status_text = tk.Text(output_frame, wrap=tk.WORD)
status_text.grid(row=0, column=0, sticky="nsew")

vertical_scroll = tk.Scrollbar(output_frame, orient=tk.VERTICAL, command=status_text.yview)
vertical_scroll.grid(row=0, column=1, sticky="ns")

horizontal_scroll = tk.Scrollbar(output_frame, orient=tk.HORIZONTAL, command=status_text.xview)
horizontal_scroll.grid(row=1, column=0, sticky="ew")

status_text.config(yscrollcommand=vertical_scroll.set, xscrollcommand=horizontal_scroll.set)
output_frame.grid_rowconfigure(0, weight=1)
output_frame.grid_columnconfigure(0, weight=1)

bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

save_button = tk.Button(bottom_frame, text="Save Output to Desktop", command=save_output_to_desktop)
save_button.pack()

wake_device()
update_status()

root.mainloop()
