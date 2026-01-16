# ==============================
# Nurse, Doctor, and Patient Data
# ==============================
from werkzeug.security import generate_password_hash


nurses = {
    "N001": {
        "nurse_id": "N001",
        "name": "Nusrat Islam",
        "age": 28,
        "gender": "Female",
        "shift": "Day",
        "assigned_room": "R101",
        "phone": "+8801711223344",
        "join_date": "2021-03-10",
        "email": "nusrat.islam@medidispense.com",
        "password": generate_password_hash("1234"),
        "education": [
            {
                "year": 2018,
                "degree": "Bachelor of Science in Nursing",
                "institute": "Dhaka Nursing College",
                "result": "Passed with Distinction"
            },
            {
                "year": 2015,
                "degree": "Diploma in General Nursing",
                "institute": "Bangladesh Nursing Council",
                "result": "Completed"
            }
        ],
        "experience": [
            {
                "year": "2020 - Present",
                "position": "Registered Nurse",
                "department": "General Ward",
                "hospital": "Dhaka Medical College Hospital"
            },
            {
                "year": "2018 - 2020",
                "position": "Junior Nurse",
                "department": "Pediatrics",
                "hospital": "Square Hospital"
            }
        ],
        "assigned_patients": ["P001", "P002", "P006", "P007"]
    },

    "N002": {
        "nurse_id": "N002",
        "name": "Fatema Khatun",
        "age": 31,
        "gender": "Female",
        "shift": "Night",
        "assigned_room": "R202",
        "phone": "+8801788992233",
        "join_date": "2020-06-15",
        "email": "fatema.khatun@medidispense.com",
        "password": generate_password_hash("5678"),
        "education": [
            {
                "year": 2016,
                "degree": "Bachelor of Science in Nursing",
                "institute": "Rajshahi Nursing College",
                "result": "Passed with Merit"
            },
            {
                "year": 2013,
                "degree": "Diploma in Nursing Science & Midwifery",
                "institute": "Bangladesh Nursing Council",
                "result": "Completed"
            }
        ],
        "experience": [
            {
                "year": "2021 - Present",
                "position": "Senior Nurse",
                "department": "ICU",
                "hospital": "Rajshahi Medical College Hospital"
            },
            {
                "year": "2017 - 2021",
                "position": "Staff Nurse",
                "department": "Emergency Ward",
                "hospital": "Green Life Hospital"
            }
        ],
        "assigned_patients": ["P008", "P009", "P010"]
    }
}

# ==============================
# Doctors
# ==============================

doctors = {
    "D001": {
        "doctor_id": "D001",
        "name": "Dr. Imran Hossain",
        "specialization": "Pulmonology",
        "department": "Respiratory Medicine",
        "age": 45,
        "gender": "Male",
        "shift": "Day",
        "room_id": "R210",
        "experience": 12,

        "qualifications": [
            {"year": 2003, "degree": "MBBS", "institution": "Dhaka Medical College"},
            {"year": 2009, "degree": "MD (Pulmonology)", "institution": "BSMMU"},
            {"year": 2015, "degree": "FCPS", "institution": "BCPS"},
            {"year": 2018, "degree": "MBA (Hospital Management)", "institution": "IUB"},
        ],

        "publications": [
            {"title": "Effectiveness of Non-Invasive Ventilation in COPD Patients", "journal": "Chest Journal", "year": 2019},
            {"title": "Role of Biomarkers in Chronic Pulmonary Disease", "journal": "Pulmonary Research Journal", "year": 2021},
        ],

        "experience": [
            {"year": "2010–2015", "position": "Junior Consultant", "department": "Pulmonology", "hospital": "Square Hospital"},
            {"year": "2016–2024", "position": "Senior Consultant", "department": "Pulmonology", "hospital": "Dhaka Medical College Hospital"},
        ],

        "email": "imran.hossain@medidispense.com",
        "phone": "+8801711001122",
        "password": generate_password_hash("doc123"),
    },

    "D002": {
        "doctor_id": "D002",
        "name": "Dr. Nusrat Jahan",
        "specialization": "Endocrinology",
        "department": "Endocrine Medicine",
        "age": 40,
        "gender": "Female",
        "shift": "Day",
        "room_id": "R215",
        "experience": 9,

        "qualifications": [
            {"year": 2005, "degree": "MBBS", "institution": "Sylhet Medical College"},
            {"year": 2011, "degree": "MD (Endocrinology)", "institution": "BSMMU"},
            {"year": 2017, "degree": "MRCP (UK)", "institution": "Royal College of Physicians"},
        ],

        "publications": [
            {"title": "Advances in Diabetes Type-II Management", "journal": "Clinical Endocrine Review", "year": 2020},
            {"title": "Endocrine Disorders in Women", "journal": "Journal of Endocrinology", "year": 2022},
        ],

        "experience": [
            {"year": "2012–2018", "position": "Endocrinologist", "department": "Medicine", "hospital": "Square Hospital"},
            {"year": "2019–2024", "position": "Senior Endocrinologist", "department": "Endocrinology", "hospital": "United Hospital"},
        ],

        "email": "nusrat.jahan@medidispense.com",
        "phone": "+8801700112233",
        "password": generate_password_hash("doc234"),
    },

    "D003": {
        "doctor_id": "D003",
        "name": "Dr. Farhana Akter",
        "specialization": "Respiratory Medicine",
        "department": "Pulmonology",
        "age": 43,
        "gender": "Female",
        "shift": "Night",
        "room_id": "R220",
        "experience": 15,

        "qualifications": [
            {"year": 2004, "degree": "MBBS", "institution": "Chittagong Medical College"},
            {"year": 2010, "degree": "DTCD", "institution": "BSMMU"},
            {"year": 2015, "degree": "MD (Respiratory Medicine)", "institution": "BSMMU"},
        ],

        "publications": [
            {"title": "Tuberculosis Treatment Challenges", "journal": "South Asian Medical Journal", "year": 2018},
            {"title": "Allergic Respiratory Disorders", "journal": "Respiratory Sciences", "year": 2021},
        ],

        "experience": [
            {"year": "2008–2014", "position": "Registrar", "department": "Respiratory Medicine", "hospital": "CMCH"},
            {"year": "2015–2024", "position": "Consultant", "department": "Respiratory Medicine", "hospital": "Evercare Hospital"},
        ],

        "email": "farhana.akter@medidispense.com",
        "phone": "+8801711888999",
        "password": generate_password_hash("doc345"),
    },

    "D004": {
        "doctor_id": "D004",
        "name": "Dr. Rafiq Rahman",
        "specialization": "Critical Care",
        "department": "ICU & Critical Care",
        "age": 50,
        "gender": "Male",
        "shift": "Night",
        "room_id": "R305",
        "experience": 18,

        "qualifications": [
            {"year": 1998, "degree": "MBBS", "institution": "Rangpur Medical College"},
            {"year": 2004, "degree": "MD (Critical Care Medicine)", "institution": "BSMMU"},
            {"year": 2010, "degree": "FCCM", "institution": "Society of Critical Care Medicine"},
        ],

        "publications": [
            {"title": "Sepsis Management in ICU", "journal": "Critical Medicine Review", "year": 2017},
            {"title": "Advancements in Ventilator Strategies", "journal": "Critical Care Journal", "year": 2022},
        ],

        "experience": [
            {"year": "2005–2015", "position": "ICU Specialist", "department": "Critical Care", "hospital": "Square Hospital"},
            {"year": "2016–2024", "position": "Senior ICU Consultant", "department": "ICU & Critical Care", "hospital": "Apollo Hospital"},
        ],

        "email": "rafiq.rahman@medidispense.com",
        "phone": "+8801711334455",
        "password": generate_password_hash("doc456"),
    },

}

patients = {

    "P001": {
        "patient_id": "P001",
        "name": "Ayesha Rahman",
        "gender": "Female",
        "age": 34,
        "weight": "62 kg",
        "height": "160 cm",
        "room": "R101",
        "diagnosis": "Pneumonia",
        "doctor": "Dr. Imran Hossain",

        "allergies": ["Penicillin"],
        "vitals": {
            "blood_pressure": "118/76",
            "heart_rate": "82 bpm",
            "temperature": "99.1°F",
            "respiration_rate": "20/min",
            "spo2": "95%"
        },

        "emergency_contact": {
            "name": "Rahim Rahman",
            "relation": "Husband",
            "phone": "+8801712345678"
        },

        "admission_date": "2025-12-05",
        "condition": "Under Observation",

        "treatments": [
            "Nebulization – 3 times daily",
            "Antibiotic therapy"
        ],

        "current_medications": [
            {"name": "Azithromycin", "dose": "500mg", "frequency": "Once daily"},
            {"name": "Paracetamol", "dose": "500mg", "frequency": "If fever > 100°F"}
        ],

        "notes": "Monitor SPO2 and respiratory rate every 2 hours.",

        "medication_schedule": ["11:40 AM", "11:48 AM", "01:30 PM", "02:16 PM", "11:00 PM"],
        "current_index": 0,
        "next_medicine_time": "11:00 AM",
        "status": "Due",
        "last_updated": None,
        "history": []
    },


    "P002": {
        "patient_id": "P002",
        "name": "Rafiq Ahmed",
        "gender": "Male",
        "age": 52,
        "weight": "74 kg",
        "height": "167 cm",
        "room": "R101",
        "diagnosis": "Type 2 Diabetes",
        "doctor": "Dr. Nusrat Jahan",

        "allergies": [],
        "vitals": {
            "blood_pressure": "130/85",
            "heart_rate": "76 bpm",
            "temperature": "98.4°F",
            "respiration_rate": "16/min",
            "spo2": "98%"
        },

        "emergency_contact": {
            "name": "Fatema Ahmed",
            "relation": "Wife",
            "phone": "+8801719988776"
        },

        "admission_date": "2025-12-06",
        "condition": "Stable",

        "treatments": [
            "Insulin monitoring",
            "Daily glucose check"
        ],

        "current_medications": [
            {"name": "Metformin", "dose": "850mg", "frequency": "Twice daily"},
            {"name": "Insulin", "dose": "10 units", "frequency": "Before breakfast"}
        ],

        "notes": "Check blood glucose before every meal.",

        "medication_schedule": ["11:39 AM", "11:47 AM", "02:17 PM", "11:00 PM"],
        "current_index": 0,
        "next_medicine_time": "07:30 AM",
        "status": "Due",
        "last_updated": None,
        "history": []
    },


    "P006": {
        "patient_id": "P006",
        "name": "Nabila Khatun",
        "gender": "Female",
        "age": 29,
        "weight": "55 kg",
        "height": "158 cm",
        "room": "R101",
        "diagnosis": "Bronchitis",
        "doctor": "Dr. Farhana Akter",

        "allergies": ["Dust"],
        "vitals": {
            "blood_pressure": "115/70",
            "heart_rate": "88 bpm",
            "temperature": "99.0°F",
            "respiration_rate": "22/min",
            "spo2": "94%"
        },

        "emergency_contact": {
            "name": "Shahidul Khatun",
            "relation": "Husband",
            "phone": "+8801788112233"
        },

        "admission_date": "2025-12-07",
        "condition": "Under Observation",

        "treatments": [
            "Bronchodilator therapy",
            "Steam inhalation"
        ],

        "current_medications": [
            {"name": "Salbutamol", "dose": "2 puffs", "frequency": "Every 6 hours"},
            {"name": "Cough syrup", "dose": "10ml", "frequency": "3 times daily"}
        ],

        "notes": "Encourage hydration.",

        "medication_schedule": ["1:08 AM", "10:00 AM", "03:00 PM", "11:57 PM"],
        "current_index": 0,
        "next_medicine_time": "10:00 AM",
        "status": "Due",
        "last_updated": None,
        "history": []
    },


    "P007": {
        "patient_id": "P007",
        "name": "Rashed Khan",
        "gender": "Male",
        "age": 41,
        "weight": "70 kg",
        "height": "170 cm",
        "room": "R101",
        "diagnosis": "Flu",
        "doctor": "Dr. Imran Hossain",

        "allergies": [],
        "vitals": {
            "blood_pressure": "120/78",
            "heart_rate": "80 bpm",
            "temperature": "101.2°F",
            "respiration_rate": "18/min",
            "spo2": "97%"
        },

        "emergency_contact": {
            "name": "Sultana Khan",
            "relation": "Wife",
            "phone": "+8801766988899"
        },

        "admission_date": "2025-12-05",
        "condition": "Stable",

        "treatments": [
            "Antiviral course",
            "Rest & hydration therapy"
        ],

        "current_medications": [
            {"name": "Oseltamivir", "dose": "75mg", "frequency": "Twice daily"},
            {"name": "Paracetamol", "dose": "500mg", "frequency": "If fever persists"}
        ],

        "notes": "High fever noted. Monitor temperature every 4 hours.",

        "medication_schedule": ["10:00 AM", "12:00 PM", "04:00 PM", "11:58 PM"],
        "current_index": 0,
        "next_medicine_time": "10:00 AM",
        "status": "Due",
        "last_updated": None,
        "history": []
    },


    "P008": {
        "patient_id": "P008",
        "name": "Sadia Rahman",
        "gender": "Female",
        "age": 22,
        "weight": "50 kg",
        "height": "155 cm",
        "room": "R202",
        "diagnosis": "Asthma",
        "doctor": "Dr. Rafiq Rahman",

        "allergies": ["Smoke"],
        "vitals": {
            "blood_pressure": "110/72",
            "heart_rate": "90 bpm",
            "temperature": "98.9°F",
            "respiration_rate": "24/min",
            "spo2": "93%"
        },

        "emergency_contact": {
            "name": "Hasina Rahman",
            "relation": "Mother",
            "phone": "+8801799994455"
        },

        "admission_date": "2025-12-07",
        "condition": "Critical",

        "treatments": [
            "Oxygen therapy",
            "Nebulizer every 4 hours"
        ],

        "current_medications": [
            {"name": "Montelukast", "dose": "10mg", "frequency": "Once daily"},
            {"name": "Inhaled corticosteroids", "dose": "2 puffs", "frequency": "Morning & night"}
        ],

        "notes": "Critical breathing difficulty earlier. High-priority monitoring.",

        "medication_schedule": ["10:00 AM", "10:00 PM"],
        "current_index": 0,
        "next_medicine_time":  "10:00 AM",
        "status": "Due",
        "last_updated": None,
        "history": []
    },


    "P009": {
        "patient_id": "P009",
        "name": "Arif Chowdhury",
        "gender": "Male",
        "age": 60,
        "weight": "80 kg",
        "height": "169 cm",
        "room": "R202",
        "diagnosis": "Hypertension",
        "doctor": "Dr. Nusrat Jahan",

        "allergies": ["Aspirin"],
        "vitals": {
            "blood_pressure": "145/92",
            "heart_rate": "85 bpm",
            "temperature": "98.5°F",
            "respiration_rate": "15/min",
            "spo2": "97%"
        },

        "emergency_contact": {
            "name": "Shamima Chowdhury",
            "relation": "Wife",
            "phone": "+8801712338899"
        },

        "admission_date": "2025-12-06",
        "condition": "Under Observation",

        "treatments": [
            "BP monitoring",
            "Salt-restricted diet"
        ],

        "current_medications": [
            {"name": "Amlodipine", "dose": "5mg", "frequency": "Once daily"}
        ],

        "notes": "BP fluctuations noted. Avoid aspirin due to allergy.",

        "medication_schedule": ["10:30 AM", "11:30 AM", "10:30 PM"],
        "current_index": 0,
        "next_medicine_time": "11:30 PM",
        "status": "Due",
        "last_updated": None,
        "history": []
    },


    "P010": {
        "patient_id": "P010",
        "name": "Shila Akter",
        "gender": "Female",
        "age": 33,
        "weight": "58 kg",
        "height": "162 cm",
        "room": "R202",
        "diagnosis": "Migraine",
        "doctor": "Dr. Imran Hossain",

        "allergies": [],
        "vitals": {
            "blood_pressure": "112/74",
            "heart_rate": "72 bpm",
            "temperature": "98.1°F",
            "respiration_rate": "17/min",
            "spo2": "98%"
        },

        "emergency_contact": {
            "name": "Rahila Akter",
            "relation": "Sister",
            "phone": "+8801788556677"
        },

        "admission_date": "2025-12-07",
        "condition": "Stable",

        "treatments": [
            "Pain management therapy",
            "Hydration therapy"
        ],

        "current_medications": [
            {"name": "Sumatriptan", "dose": "50mg", "frequency": "As needed"},
            {"name": "Ibuprofen", "dose": "400mg", "frequency": "As needed"}
        ],

        "notes": "Avoid bright light exposure. Provide quiet environment.",

        "medication_schedule": ["12:00 AM", "06:00 AM", "11:00 PM"],
        "current_index": 0,
        "next_medicine_time": "12:00 AM",
        "status": "Due",
        "last_updated": None,
        "history": []
    }

}

