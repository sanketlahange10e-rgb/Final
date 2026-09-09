import csv
from pathlib import Path
from tkinter import messagebox
from MYLIB.modules.PassHash import encrypt_password, verify_password

# Base directory
base_dir = Path(__file__).resolve().parent.parent / "data"

# Role → file mapping
FILE_MAP = {
    "Student": "stdcood3.csv",
    "Admin": "Admin.csv",
    "Driver": "Driver.csv"
}


# -------------------------------
# 🔍 GET ACCOUNT DETAILS (LOGIN)
# -------------------------------
def get_account_details(username, password, role):
    file_path = base_dir / FILE_MAP.get(role, "")

    if not file_path.exists():
        return {'success': False, 'message': 'File not found'}

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            if row.get("username") == username:
                if verify_password(password, row.get("password")):
                    return {
                        'success': True,
                        'data': row
                    }
                else:
                    return {'success': False, 'message': 'Wrong password'}

    return {'success': False, 'message': 'User not found'}


# -------------------------------
# ✏️ UPDATE ACCOUNT DETAILS
# -------------------------------
def update_account_details(prnNo, username, password, new_password, role):
    file_path = base_dir / FILE_MAP.get(role, "")

    if not file_path.exists():
        return {'success': False, 'message': 'File not found'}

    rows = []
    updated = False

    with open(file_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        for row in reader:
            match = False

            if role == "Student":
                match = row.get("prn_no") == prnNo
            else:
                match = row.get("username") == username

            if match and verify_password(password, row.get("password")):
                row["username"] = username
                row["password"] = encrypt_password(new_password)
                updated = True

            rows.append(row)

    if not updated:
        return {'success': False, 'message': 'Invalid credentials'}

    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return {'success': True, 'message': 'Account updated successfully'}


# -------------------------------
# 🔍 CHECK USERNAME EXISTS
# -------------------------------
def username_exists(file_path, username):
    if not file_path.exists():
        return False

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("username") == username:
                return True
    return False


# -------------------------------
# 💾 SAVE ACCOUNT DETAILS (SIGNUP)
# -------------------------------
def save_account_details(prnNo, name, username, password, latitude, longitude, role):
    file_path = base_dir / FILE_MAP.get(role, "")

    # Ensure file exists with proper headers
    if not file_path.exists():
        with open(file_path, 'w', newline='') as f:
            if role == "Student":
                fieldnames = ["prn_no", "name", "username", "password", "latitude", "longitude"]
            else:
                fieldnames = ["username", "password"]

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

    # Check username
    if username_exists(file_path, username):
        messagebox.showwarning("Signup Failed", "Username already exists")
        return {'success': False}

    with open(file_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=None)

        if role == "Student":
            writer = csv.DictWriter(f, fieldnames=["prn_no", "name", "username", "password", "latitude", "longitude"])
            writer.writerow({
                "prn_no": prnNo,
                "name": name,
                "username": username,
                "password": encrypt_password(password),
                "latitude": latitude,
                "longitude": longitude
            })
        else:
            writer = csv.DictWriter(f, fieldnames=["username", "password"])
            writer.writerow({
                "username": username,
                "password": encrypt_password(password)
            })

    messagebox.showinfo("Signup Success", "Account created successfully")
    return {'success': True}