# MediDispense
# MediDispense — Smart Medication Tracking System

MediDispense is a Python-based medication management application designed to help healthcare staff monitor patient medication schedules and track medication administration. The system provides a web-based interface for managing medication records and a desktop touchscreen-style interface for viewing upcoming doses and updating medication status.

## Features

- **Role-Based Access:** Separate access for nurses and doctors.
- **Medication Scheduling:** Displays upcoming medication doses based on patient schedules.
- **Administration Tracking:** Records medication status, including given and missed doses.
- **Real-Time Notifications:** Supports medication alert events using Flask-SocketIO.
- **Desktop Interface:** Provides a Tkinter-based interface for viewing upcoming doses and interacting with the dispensing workflow.
- **Patient Reports:** Generates downloadable PDF summaries containing patient and medication information.
- **Hardware Integration:** Includes optional Arduino serial communication for future physical dispensing integration.

## Technology Stack

- **Language:** Python
- **Backend Framework:** Flask
- **Desktop GUI:** Tkinter
- **Real-Time Communication:** Flask-SocketIO
- **HTTP Requests:** Requests
- **PDF Generation:** ReportLab
- **Data Storage:** JSON-based medication history
- **Hardware Communication:** PySerial (optional)

## Project Repository

[View the source code on GitHub](https://github.com/Prova12345-byte/MediDispense)
