# backend/auth.py

from backend.data_store import nurses, doctors

def check_nurse_login(nurse_id):
    """
    Verifies nurse ID and returns nurse info if found.
    """
    if nurse_id in nurses:
        return nurses[nurse_id]
    return None


def check_doctor_login(doctor_id):
    """
    Verifies doctor ID and returns doctor info if found.
    """
    if doctor_id in doctors:
        return doctors[doctor_id]
    return None
