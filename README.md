# TaskFlow 🧭 — Minimal Task & Project Manager

A clean and modern productivity web application that helps users create tasks, organize projects, and track progress — built with **Flask**, **SQLAlchemy**, and a **Tailwind-powered UI**.

🔗 **Live Demo:** https://taskflow-95hh.onrender.com  
📦 **GitHub Repo:** https://github.com/Fb-JAYRAJ/TaskFlow  

---

## 🚀 Features

### ✔ User Accounts
- Register / Login / Logout  
- Secure authentication (hashed passwords)  
- Session-based login with Flask-Login  

### ✔ Task Management
- Create, edit, and manage tasks  
- Add descriptions & due dates  
- Track completed tasks  
- Dashboard shows recent tasks  

### ✔ Project Management
- Create projects  
- Group tasks under specific projects  
- Project-wise task view  

### ✔ Clean Dashboard
- Weekly & monthly task stats  
- Active projects  
- Recent tasks  
- Quick actions (New Task, New Project)  

### ✔ Modern UI
- Tailwind CSS  
- Alpine.js interactions  
- Fully responsive  
- Dark/Light mode toggle  

### ✔ Deployment Ready
- Deployed on Render  
- Gunicorn as production server  
- SQLite database stored safely in `/tmp` path  

---

## 🧱 Tech Stack

### **Frontend**
- Jinja2 Templates  
- Tailwind CSS  
- Alpine.js  

### **Backend**
- Flask  
- Flask-SQLAlchemy  
- Flask-Migrate  
- Flask-Login  
- Flask-WTF  

### **Database**
- SQLite (local + Render persistent runtime path)

### **Deployment**
- Render Web Service  
- Gunicorn  

---

## 📂 Project Structure
```
TaskFlow/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── extensions.py
│   ├── blueprints/
│   │   ├── auth/
│   │   ├── core/
│   │   └── dashboard/
│   └── templates/
│       ├── base.html
│       ├── base_public.html
│       ├── index.html
│       ├── auth/
│       ├── dashboard/
├── static/
│   └── css/app.css
├── requirements.txt
├── run.py
└── README.md
```

---

## ⚙️ Setup Instructions (Local Development)

### 1️⃣ Clone the repo
```
git clone https://github.com/Fb-JAYRAJ/TaskFlow.git
cd TaskFlow
```

### 2️⃣ Create a virtual environment
```
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# or: venv\Scripts\activate  # Windows
```

### 3️⃣ Install dependencies
```
pip install -r requirements.txt
```
### 4️⃣ Create a .env file
```
SECRET_KEY=your-secret-key
FLASK_ENV=development
```

### 5️⃣ Initialize the database
```
mkdir -p instance
flask db upgrade
```

### 6️⃣ Run the application
```
flask run
```

## 📌 Future Improvements
- Task labels & priority system  
- Drag-and-drop task sorting  
- Project analytics  
- OAuth login (Google / GitHub)  
- Public API endpoints  
⸻

## 🙌 Author

Jayraj Sawant
Full-stack Developer — Flask • React • SQL
GitHub: https://github.com/Fb-JAYRAJ
