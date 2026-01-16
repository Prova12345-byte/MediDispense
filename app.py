from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from backend.data_store import doctors, nurses, patients
from werkzeug.security import check_password_hash
from flask_socketio import SocketIO
from datetime import datetime, timedelta
import pytz, json
import json, os
from flask import Response, make_response

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from flask import send_file
import io





# ----------------------------- TIMEZONE -----------------------------

# ==================== HISTORY SYSTEM ======================
HISTORY_FILE = "history_store.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_history(data):
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

 # Load saved history into memory
saved_history = load_history()

for pid, p in patients.items():
    # Keep patient dictionary intact — ONLY replace its history list
    p["history"] = saved_history.get(pid, p.get("history", []))

    # Ensure proper type (avoid corruption)
    if not isinstance(p["history"], list):
        p["history"] = []




BD = pytz.timezone("Asia/Dhaka")
LOCK_MINUTES = 2

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
app.secret_key = "medidispense_secret_key"


# ============================= HELPERS ==============================

def bd_now():
    return datetime.now(BD)


def log_history(patient, action, status, dose_time=None):
    now = bd_now()

    # Missed dose event time = scheduled date only
    if status == "Missed":
        event_time = now.strftime("%Y-%m-%d")   # date only
    else:
        event_time = now.strftime("%Y-%m-%d")   # date only for normal actions too

    entry = {
        "patient_id": patient["patient_id"],
        "patient_name": patient["name"],
        "dose_time": dose_time,
        "time": event_time,     # ONLY DATE
        "action": action,
        "status": status
    }

    patient.setdefault("history", [])
    patient["history"].append(entry)

    # Save to file
    all_history = {pid: p.get("history", []) for pid, p in patients.items()}
    save_history(all_history)

def refresh_patient_schedule(patient):
    schedule = patient.get("medication_schedule", [])
    if not schedule:
        patient["next_medicine_time"] = None
        return

    now = bd_now().replace(second=0, microsecond=0)

    idx = patient.get("current_index", 0)
    if idx >= len(schedule):
        idx = 0
        patient["current_index"] = 0

    for _ in range(len(schedule)):  # loop MAX schedule length (no infinite loop)
        t_str = schedule[idx]
        t_parsed = datetime.strptime(t_str, "%I:%M %p")

        scheduled_dt = now.replace(
            hour=t_parsed.hour,
            minute=t_parsed.minute,
            second=0,
            microsecond=0
        )

        lock_time = scheduled_dt + timedelta(minutes=LOCK_MINUTES)

        # CASE 1 — Too early
        if now < scheduled_dt:
            patient["next_medicine_time"] = t_str
            patient["status"] = "Due"
            return

        # CASE 2 — Within allowed window
        if scheduled_dt <= now <= lock_time:
            patient["next_medicine_time"] = t_str
            return

        # CASE 3 — Missed
        already_logged = any(
            h.get("dose_time") == t_str and h.get("status") == "Missed"
            for h in patient.get("history", [])
        )

        if not already_logged and patient["status"] != "Given":
            log_history(patient, "Missed Dose", "Missed", dose_time=t_str)

        # move to next dose
        idx = (idx + 1) % len(schedule)
        patient["current_index"] = idx

    # CASE 4 — All doses passed → tomorrow's first
    patient["next_medicine_time"] = schedule[0]
    patient["status"] = "Due"







# ============================ AUTH ROUTES ===========================

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")
        rfid = request.form.get("rfid", "").strip().replace("RFID-", "")
        password = request.form.get("password")

        if not role or not rfid or not password:
            return render_template("login.html", error="All fields are required")

        user = nurses.get(rfid) if role.lower() == "nurse" else doctors.get(rfid)

        if user and check_password_hash(user["password"], password):
            session["role"] = role.lower()
            session["user_id"] = rfid
            session["user"] = user

            if session["role"] == "nurse":
                return redirect(url_for("nurse_profile", nurse_id=rfid))
            else:
                return redirect(url_for("doctor_profile", doctor_id=rfid))

        return render_template("login.html", error="Invalid RFID or Password")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# =========================== NURSE ROUTES ===========================

@app.route("/nurse/<nurse_id>")
def nurse_profile(nurse_id):
    nurse = nurses.get(nurse_id)
    if not nurse:
        return "Nurse not found", 404

    session["role"] = "nurse"
    session["user"] = nurse
    return render_template("nurse_profile.html", nurse=nurse)


@app.route("/nurse_dashboard")
def nurse_dashboard():
    nurse_id = session.get("user_id")

    if not nurse_id or session.get("role") != "nurse":
        return redirect(url_for("login"))

    nurse = nurses.get(nurse_id)   # ALWAYS fetch fresh nurse

    assigned_list = nurse.get("assigned_patients", [])
    if isinstance(assigned_list, str):
        assigned_list = [assigned_list]

    assigned_patients = []
    for pid in assigned_list:
        if pid in patients:
            p = patients[pid]
            refresh_patient_schedule(p)

            assigned_patients.append(p)

    return render_template(
        "nurse_dashboard.html",
        nurse=nurse,
        assigned_patients=assigned_patients,
        last_updated=session.get("nurse_last_action")
    )







@app.route("/nurse_patients")
def nurse_patients():
    nurse_id = session.get("user_id")

    if not nurse_id or session.get("role") != "nurse":
        return redirect(url_for("login"))

    nurse = nurses.get(nurse_id)

    assigned_list = nurse.get("assigned_patients", [])
    if isinstance(assigned_list, str):
        assigned_list = [assigned_list]

    assigned_patients = []
    for pid in assigned_list:
        if pid in patients:
            refresh_patient_schedule(patients[pid])
            assigned_patients.append(patients[pid])

    return render_template("nurse_patients.html",
                           nurse=nurse,
                           assigned_patients=assigned_patients)



@app.route('/patient/<patient_id>')
def patient_profile(patient_id):
    patient = patients.get(patient_id)

    nurse_id = session.get("nurse_id")
    nurse = nurses.get(nurse_id)

    return render_template("patient_profile.html", patient=patient, nurse=nurse)


@app.route("/export_pdf/<patient_id>")
def export_pdf(patient_id):
    patient = patients.get(patient_id)
    if not patient:
        return "Patient not found", 404

    # Memory buffer for PDF
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"{patient_id}_EMR_Report")

    # PDF styling
    x = 50
    y = 750
    line_height = 16

    def write(text, bold=False, space=0):
        nonlocal y
        if bold:
            pdf.setFont("Helvetica-Bold", 12)
        else:
            pdf.setFont("Helvetica", 11)

        pdf.drawString(x, y, text)
        y -= line_height + space

    # HEADER
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, 800, "MediDispense – Patient Summary Report")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 780, f"Patient ID: {patient_id}")
    pdf.line(50, 775, 560, 775)

    # Patient Basic Info
    write("=== Patient Information ===", bold=True, space=6)
    write(f"Name: {patient['name']}")
    write(f"Gender: {patient['gender']}")
    write(f"Room: {patient['room']}")
    write(f"Diagnosis: {patient['diagnosis']}")
    write("")

    # Vitals
    vitals = patient.get("vitals", {})
    write("=== Vitals ===", bold=True, space=6)
    write(f"Blood Pressure: {vitals.get('bp', '—')}")
    write(f"Heart Rate: {vitals.get('hr', '—')} bpm")
    write(f"Temperature: {vitals.get('temp', '—')}°F")
    write("")

    # Medication Schedule
    write("=== Medication Schedule ===", bold=True, space=6)
    write(f"Next Dose: {patient['next_medicine_time']}")
    write(f"Status: {patient['status']}")
    write("")

    # Current Medications
    write("=== Current Medications ===", bold=True, space=6)
    for med in patient.get("current_medications", []):
        write(f"- {med}")
    write("")

    # Ongoing Treatments
    write("=== Ongoing Treatments ===", bold=True, space=6)
    for t in patient.get("treatments", []):
        write(f"- {t}")
    write("")

    # Allergies
    write("=== Allergies ===", bold=True, space=6)
    for a in patient.get("allergies", []):
        write(f"- {a}")
    write("")

    # Clinical Notes
    write("=== Clinical Notes ===", bold=True, space=6)
    write(patient.get("notes", "No notes available."))

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{patient_id}_EMR_Report.pdf",
        mimetype="application/pdf"
    )





# =========================== DOCTOR ROUTES ===========================

@app.route("/doctor/<doctor_id>")
def doctor_profile(doctor_id):
    doctor = doctors.get(doctor_id)
    if not doctor:
        return "Doctor not found", 404

    session["role"] = "doctor"
    session["user_id"] = doctor_id
    session["user"] = doctor

    return render_template("doctor_profile.html", doctor=doctor)


@app.route("/doctor_dashboard/<doctor_id>")
def doctor_dashboard(doctor_id):
    if session.get("role") != "doctor":
        return redirect(url_for("login"))

    doctor = doctors.get(doctor_id)
    session["user_id"] = doctor_id

    assigned_patients = [
        p for p in patients.values() if p["doctor"] == doctor["name"]
    ]

    for p in assigned_patients:
        refresh_patient_schedule(p)

    return render_template("doctor_dashboard.html",
                           doctor=doctor,
                           assigned_patients=assigned_patients)


@app.route("/doctor_my_patients/<doctor_id>")
def doctor_my_patients(doctor_id):
    if session.get("role") != "doctor":
        return redirect(url_for("login"))

    doctor = doctors.get(doctor_id)
    session["user_id"] = doctor_id

    assigned_patients = [
        p for p in patients.values() if p["doctor"] == doctor["name"]
    ]

    return render_template("doctor_my_patients.html",
                           doctor=doctor,
                           assigned_patients=assigned_patients)


@app.route("/doctor_history/<doctor_id>")
def doctor_history(doctor_id):
    doctor = doctors.get(doctor_id)
    session["user_id"] = doctor_id

    history = []
    for p in patients.values():
        if p["doctor"] == doctor["name"]:
            for h in p["history"]:
                history.append({
                    "patient_id": p["patient_id"],
                    "patient_name": p["name"],
                    "dose_time": h["dose_time"],
                    "time": h["time"],
                    "action": h["action"],
                    "status": h["status"],
                })

    return render_template("doctor_history.html",
                           doctor=doctor,
                           history_json=json.dumps(history))






# ========================= MEDICINE STATUS ===========================

@app.route("/update_medicine_status", methods=["POST"])
def update_medicine_status():
    try:
        data = request.get_json()
        patient_id = data.get("patient_id")

        # 1) Basic validation
        if patient_id not in patients:
            return jsonify({"success": False, "message": "Invalid patient"}), 400

        patient = patients[patient_id]

        schedule = patient.get("medication_schedule", [])
        if not schedule or not isinstance(schedule, list):
            return jsonify({"success": False, "message": "No schedule found"}), 400

        # Make sure current_index is safe
        idx = patient.get("current_index", 0)
        if not isinstance(idx, int) or idx < 0 or idx >= len(schedule):
            idx = 0
            patient["current_index"] = 0

        # Current BD time, rounded to the nearest minute
        now = bd_now().replace(second=0, microsecond=0)

        # Current dose time string, e.g. "08:49 PM"
        t_str = schedule[idx]
        t_parsed = datetime.strptime(t_str, "%I:%M %p")

        # Scheduled datetime (today at that time, in BD tz)
        scheduled_dt = now.replace(
            hour=t_parsed.hour,
            minute=t_parsed.minute,
            second=0,
            microsecond=0
        )

        # STRICT WINDOW: from scheduled_dt to scheduled_dt + LOCK_MINUTES
        lock_time = scheduled_dt + timedelta(minutes=LOCK_MINUTES)

        # 🔒 RULE 1 — EARLY: cannot give before scheduled time
        if now < scheduled_dt:
            return jsonify({
                "success": False,
                "message": f"Cannot give before scheduled time ({t_str})."
            })

        # 🔒 RULE 2 — LOCKED: more than LOCK_MINUTES after scheduled time
        # Allowed window is: scheduled_dt <= now <= lock_time
        if now > lock_time:
            # Mark as Missed (only once)
            already_logged = any(
                h.get("dose_time") == t_str and h.get("status") == "Missed"
                for h in patient.get("history", [])
            )
            if not already_logged:
                log_history(patient, "Missed Dose", "Missed", dose_time=t_str)

            # Move schedule forward & compute next dose
            refresh_patient_schedule(patient)

            return jsonify({
                "success": False,
                "locked": True,
                "message": "This dose is locked and has been marked as missed.",
                "new_time": patient.get("next_medicine_time")
            })

        # 🎯 If we reach here, we are inside the allowed window.
        # Toggle status: Due → Given, Given → Due
        current_status = patient.get("status", "Due")
        new_status = "Given" if current_status != "Given" else "Due"
        patient["status"] = new_status

        # Log history + last_updated
        if new_status == "Given":
            log_history(patient, "Medicine Given", "Given", dose_time=t_str)
            stamp = now.strftime("%Y-%m-%d %I:%M:%S %p")
            patient["last_updated"] = stamp
            # This is what your dashboard shows at bottom
            session["nurse_last_action"] = stamp
        else:
            log_history(patient, "Status Reverted", "Due", dose_time=t_str)

        # We do NOT advance to next dose here.
        # next_medicine_time will move automatically via refresh_patient_schedule()
        # when the time passes the lock window.
        return jsonify({
            "success": True,
            "locked": False,
            "new_status": new_status,
            "new_time": patient.get("next_medicine_time"),
            "last_updated": patient.get("last_updated")
        })

    except Exception as e:
        print("ERROR in update_medicine_status:", e)
        return jsonify({"success": False, "message": "Server error"}), 500



@app.route("/update_manual_time", methods=["POST"])
def update_manual_time():
    data = request.get_json()
    pid = data.get("patient_id")
    new_time = data.get("new_time")  # example: "02:19 AM"


    if pid not in patients:
        return jsonify({"success": False, "message": "Invalid patient"}), 400


    patient = patients[pid]


    # Update the medication schedule permanently (OPTION 1)
    idx = patient.get("current_index", 0)
    try:
        # Validate time format
        datetime.strptime(new_time, "%I:%M %p")
    except:
        return jsonify({"success": False, "message": "Invalid time format"}), 400


    # Update schedule slot
    patient["medication_schedule"][idx] = new_time
    patient["next_medicine_time"] = new_time  # reflect immediately


    return jsonify({
        "success": True,
        "new_time": new_time
    })


    


   

# =========================== HISTORY ================================

@app.route("/nurse_history")
def nurse_history():
    nurse_id = session.get("user_id")

    if not nurse_id or session.get("role") != "nurse":
        return redirect(url_for("login"))

    nurse = nurses.get(nurse_id)

    assigned_list = nurse.get("assigned_patients", [])
    if isinstance(assigned_list, str):
        assigned_list = [assigned_list]

    saved_history = load_history()
    history_entries = []

    for pid in assigned_list:
        if pid in saved_history:
            for entry in saved_history[pid]:
                entry.setdefault("patient_id", pid)
                entry.setdefault("patient_name", patients[pid]["name"])
                history_entries.append(entry)

    history_entries.sort(key=lambda x: x.get("time", ""), reverse=True)

    return render_template("nurse_history.html",
                           nurse=nurse,
                           history_json=json.dumps(history_entries))
 

# ---------------- SCHEDULE CHECKER (RUNS EVERY 30 SECONDS) ------------------
from threading import Thread
import time

def schedule_monitor():
    while True:
        now = bd_now().strftime("%I:%M %p")

        for pid, patient in patients.items():
            # Compare next_medicine_time with current time
            if patient.get("next_medicine_time") == now:
                socketio.emit("medicine_alert", {
                    "patient_id": pid,
                    "patient_name": patient["name"],
                    "room": patient["room"],
                    "time": now
                })

        time.sleep(30)   # check every 30 seconds

# Start background task
thread = Thread(target=schedule_monitor)
thread.daemon = True
thread.start()


# ============================== RUN ================================

if __name__ == "__main__":
    app.run(debug=True)
