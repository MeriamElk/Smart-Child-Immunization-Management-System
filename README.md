# 🩺 VacciTrack – Smart Child Immunization Management System

**VacciTrack** is a web-based platform designed to intelligently manage and monitor child vaccination records.  
It allows parents, healthcare professionals, and administrators to track immunization schedules, receive automated reminders, and analyze vaccination coverage efficiently.

> **Developed by:** *Meriam Elk & Meriem ZAHRI*  

---

## 🚀 Features

- 🧒 **Parent Dashboard** – View children’s vaccination profiles and receive personalized reminders  
- 🩹 **Doctor Interface** – Manage vaccination records, update medical data, and generate reports  
- 🧑‍💼 **Administrator Panel** – Oversee users, permissions, and database integrity  
- 🔔 **Smart Alerts System** – Automated notifications for upcoming or missed vaccinations  
- 📊 **Analytics Dashboard** – Visual insights into vaccination coverage and performance trends  

---

## 🧰 Technical Requirements

- **Python** ≥ 3.9  
- **MySQL Server** (v8.x recommended)  
- **MongoDB** (local instance, e.g., `localhost:27017`)  
- **Pip** + **venv** for virtual environment management  

---

## ⚙️ Installation & Setup

### 1️⃣ Create and activate a virtual environment
```bash
python -m venv venv
# Activate it:
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure MySQL
Import the database schema:
```bash
mysql -u root -p < data/create_mysql_schema.sql
```

### 4️⃣ Configure MongoDB
Start MongoDB (default: localhost:27017) and initialize data:
```bash
python data/initialize_mongodb.py
```

### 5️⃣ Run the Flask application
```bash
python app.py
```

Access the interface at 👉 http://127.0.0.1:5000/

## 👥 User Roles

| Role | Description |
|------|--------------|
| 👨‍👩‍👧 **Parent** | View children’s vaccination history and receive alerts |
| 👩‍⚕️ **Doctor** | Manage vaccination records and perform data analysis |
| 🧑‍💻 **Administrator** | Manage all users, vaccines, and system configuration |


##🧪 Test Data

Includes:
Pre-created user accounts (emails + hashed passwords)
Sample children, vaccines, vaccination schedules, and alert data

## 🧱 Technologies Used

| Layer | Technologies |
|--------|---------------|
| **Backend** | Flask (Python) |
| **Database** | MySQL (SQLAlchemy ORM) & MongoDB |
| **Frontend** | Jinja2, HTML, CSS, JavaScript |
| **Security** | Bcrypt, JWT |
| **Data Handling** | REST APIs & dynamic templates |

##💡 Future Enhancements

Integration with SMS or Email notification systems
Real-time analytics dashboard for health authorities
AI-based prediction of vaccination trends and delays
