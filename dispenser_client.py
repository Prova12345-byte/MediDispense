#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
import time
import serial  # optional: comment out if no Arduino
from datetime import datetime, timedelta
from functools import partial

try:
    # Python 3.9+: prefer zoneinfo
    from zoneinfo import ZoneInfo
    HAVE_ZONEINFO = True
except Exception:
    HAVE_ZONEINFO = False

# ========================
# Configuration
# ========================
# ========================
# Configuration
# ========================
FLASK_SERVER = "http://192.168.0.105:5000"   # example: your Flask server IP
REFRESH_INTERVAL_SEC = 60
UI_TICK_SEC = 10
DUE_WINDOW_MIN = 90
USE_ARDUINO = False
SERIAL_PORT = "/dev/ttyUSB0"
SERIAL_BAUD = 9600
TIMEZONE_NAME = "Asia/Dhaka"   # GMT+6 ✅


# ========================
# Arduino (optional)
# ========================
arduino = None
if USE_ARDUINO:
    try:
        arduino = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1)
        time.sleep(2)
        print("Arduino connected.")
    except Exception as e:
        print("Arduino not connected:", e)
        arduino = None

# ========================
# Time helpers
# ========================
def now_local():
    if HAVE_ZONEINFO:
        return datetime.now(ZoneInfo(TIMEZONE_NAME))
    return datetime.now()

def parse_12h_time_to_next_dt(time_str: str):
    """
    Given '08:00 AM' -> return a datetime for the next occurrence today or tomorrow.
    Assumes local tz (ZoneInfo if available).
    """
    if not time_str:
        return None
    n = now_local()
    try:
        t = datetime.strptime(time_str.strip(), "%I:%M %p").time()
    except ValueError:
        # fallback to HH:MM (24h) if someone changes format
        try:
            t = datetime.strptime(time_str.strip(), "%H:%M").time()
        except ValueError:
            return None

    candidate = n.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
    if candidate < n:
        candidate = candidate + timedelta(days=1)
    return candidate

def human_dt(dt: datetime):
    return dt.strftime("%a %b %d, %I:%M %p")

# ========================
# Data model & selection
# ========================
patients_data = {}           # raw from Flask
current_selection = None     # dict with selected dose info

def fetch_schedule():
    global patients_data
    try:
        r = requests.get(f"{FLASK_SERVER}/get_medicine_schedule", timeout=6)
        r.raise_for_status()
        patients_data = r.json() or {}
    except Exception as e:
        print("Error fetching schedule:", e)

def expand_all_doses(patients_json):
    """
    Build a list of dose entries:
    {
      'patient_id','patient_name','diagnosis','time_label','time_str','next_dt'
    }
    time_label ∈ {'morning','afternoon','night', or arbitrary keys present}
    """
    results = []
    for pid, p in patients_json.items():
        name = p.get("patient_name", pid)
        diagnosis = p.get("diagnosis", "")
        mt = p.get("medicine_time", {}) or {}
        for label, tstr in mt.items():
            ndt = parse_12h_time_to_next_dt(tstr)
            if ndt:
                results.append({
                    "patient_id": p.get("patient_id", pid),
                    "patient_name": name,
                    "diagnosis": diagnosis,
                    "time_label": str(label).capitalize(),
                    "time_str": tstr,
                    "next_dt": ndt
                })
    # sort by closest time
    results.sort(key=lambda d: d["next_dt"])
    return results

def pick_next_due(doses):
    """
    Pick the dose that is within DUE_WINDOW_MIN from now; otherwise return the soonest upcoming.
    """
    if not doses:
        return None
    n = now_local()
    window = timedelta(minutes=DUE_WINDOW_MIN)
    # first try: something due within window
    due = [d for d in doses if d["next_dt"] - n <= window]
    if due:
        return due[0]
    # else: pick soonest upcoming
    return doses[0]

# ========================
# UI
# ========================
root = tk.Tk()
root.title("MediDispense")
root.geometry("800x480")
root.configure(bg="#e8f0ff")
root.attributes("-fullscreen", True)

# Title Bar
title = tk.Label(root, text="Smart Medicine Dispenser", font=("Poppins", 22, "bold"),
                 bg="#e8f0ff", fg="#0a4b91")
title.pack(pady=(10, 0))

subtitle = tk.Label(root, text="Touchscreen Console", font=("Poppins", 14),
                    bg="#e8f0ff", fg="#334155")
subtitle.pack(pady=(0, 10))

# Main frame
card = tk.Frame(root, bg="#ffffff", bd=0, highlightthickness=0)
card.place(relx=0.5, rely=0.53, anchor="center", width=720, height=320)

# Card content
status_label = tk.Label(card, text="Connecting to server...", font=("Poppins", 16),
                        bg="#ffffff", fg="#003366")
status_label.pack(pady=(18, 8))

patient_label = tk.Label(card, text="—", font=("Poppins", 22, "bold"),
                         bg="#ffffff", fg="#1e40af")
patient_label.pack(pady=4)

diagnosis_label = tk.Label(card, text="", font=("Poppins", 14),
                           bg="#ffffff", fg="#475569")
diagnosis_label.pack(pady=2)

time_label = tk.Label(card, text="", font=("Poppins", 16),
                      bg="#ffffff", fg="#111827")
time_label.pack(pady=8)

button_row = tk.Frame(card, bg="#ffffff")
button_row.pack(pady=18)

style = ttk.Style()
style.configure("Big.TButton", font=("Poppins", 16), padding=10)

dispense_btn = ttk.Button(button_row, text="Dispense", style="Big.TButton")
confirm_btn = ttk.Button(button_row, text="Confirm Given", style="Big.TButton")
dispense_btn.grid(row=0, column=0, padx=18)
confirm_btn.grid(row=0, column=1, padx=18)

footer = tk.Label(root,
                  text="Press ESC to exit fullscreen",
                  font=("Poppins", 10), bg="#e8f0ff", fg="#64748b")
footer.pack(side="bottom", pady=6)

# ========================
# UI Actions
# ========================
def set_selection(sel):
    global current_selection
    current_selection = sel
    if not sel:
        status_label.config(text="No upcoming doses found.")
        patient_label.config(text="—")
        diagnosis_label.config(text="")
        time_label.config(text="")
        return

    n = now_local()
    mins = int((sel["next_dt"] - n).total_seconds() // 60)
    when_txt = "due now" if mins <= 0 else f"in {mins} min"
    status_label.config(text=f"Next dose {when_txt}")
    patient_label.config(text=f"{sel['patient_name']}  ({sel['patient_id']})")
    diagnosis_label.config(text=f"Diagnosis: {sel['diagnosis'] or '—'}")
    time_label.config(text=f"{sel['time_label']}: {sel['time_str']}  →  {human_dt(sel['next_dt'])}")

def ui_tick():
    # recompute next due from current patients_data
    doses = expand_all_doses(patients_data)
    set_selection(pick_next_due(doses))
    root.after(UI_TICK_SEC * 1000, ui_tick)

def thread_fetch_loop():
    while True:
        fetch_schedule()
        time.sleep(REFRESH_INTERVAL_SEC)

def do_dispense():
    if not current_selection:
        messagebox.showwarning("No Patient", "No upcoming dose selected.")
        return
    status_label.config(text="Dispensing medicine…")
    root.update()

    if USE_ARDUINO and arduino:
        try:
            arduino.write(f"DISPENSE {current_selection['patient_id']}\n".encode())
            resp = arduino.readline().decode(errors="ignore").strip()
            print("Arduino:", resp)
        except Exception as e:
            print("Arduino error:", e)
            messagebox.showerror("Arduino Error", str(e))
            status_label.config(text="Dispense error.")
            return
    else:
        # simulate a short dispense delay
        time.sleep(2)

    status_label.config(text="Dispensing complete ✅")

def do_confirm_given():
    if not current_selection:
        messagebox.showwarning("No Patient", "No upcoming dose selected.")
        return
    pid = current_selection["patient_id"]
    try:
        r = requests.post(f"{FLASK_SERVER}/update_medicine_status",
                          json={"patient_id": pid, "status": "given"},
                          timeout=6)
        data = r.json()
        if data.get("success"):
            status_label.config(text=f"Patient {pid} marked as GIVEN ✅")
        else:
            status_label.config(text=f"Update failed: {data.get('message','Unknown error')}")
    except Exception as e:
        status_label.config(text=f"Network error: {e}")

dispense_btn.config(command=lambda: threading.Thread(target=do_dispense, daemon=True).start())
confirm_btn.config(command=lambda: threading.Thread(target=do_confirm_given, daemon=True).start())

# ========================
# Start background tasks
# ========================
# fetch thread
threading.Thread(target=thread_fetch_loop, daemon=True).start()
# first UI tick
root.after(1200, ui_tick)

# ESC exits fullscreen
def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)
root.bind("<Escape>", exit_fullscreen)

root.mainloop()
