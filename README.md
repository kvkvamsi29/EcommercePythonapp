# 🛒 E-commerce Website

A Django-based E-commerce Website where users can browse products, search for products, add items to a shopping cart, place orders, create accounts, and manage their account.

The project is built using **Python, Django, and MySQL**.

This guide explains how to clone the project, install the required packages, configure the environment, and run the website locally at:

```text
http://127.0.0.1:8000/
```

---

## 🧰 Requirements

Before starting, install:

* 🐍 Python
* 🌐 Git
* 📝 Visual Studio Code (recommended)
* 🗄️ MySQL
* 📦 pip (included with Python)

Check Python:

```bash
python --version
```

Check Git:

```bash
git --version
```

---

# 🚀 Setup Instructions

## 1️⃣ Clone the Repository

Open **Command Prompt / Terminal** and run:

```bash
git clone https://github.com/kvkvamsi29/EcommercePythonapp.git
```

Go inside the project:

```bash
cd EcommercePythonapp
```

You should see files such as:

```text
manage.py
requirements.txt
.env.example
Eshop/
store/
```

---

## 2️⃣ Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

You should see `(venv)` at the beginning of your terminal.

Example:

```text
(venv) C:\Projects\EcommercePythonapp>
```

---

## 3️⃣ Install Required Packages

Install all Python packages required by the project:

```bash
pip install -r requirements.txt
```

Wait until the installation finishes successfully.

---

# 4️⃣ Configure `.env` File 🔐

The project uses environment variables for configuration and sensitive information such as:

* 🔐 Django secret key
* 🗄️ MySQL database details
* 📧 Gmail email address
* 🔑 Gmail App Password
* 🔑 API keys

The repository contains a file named:

```text
.env.example
```

### 📌 Important: `.env.example` is a template

`.env.example` should contain **example/placeholder values only**.

For example:

```env
SECRET_KEY=replace-with-your-django-secret
DEBUG=True

DATABASE_NAME=myecomdb
DATABASE_USER=root
DATABASE_PASSWORD=replace-with-your-mysql-password
DATABASE_HOST=localhost
DATABASE_PORT=3306

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=replace-with-your-gmail-app-password

RAPIDAPI_KEY=replace-with-your-rapidapi-key
```

### Step 1 — Create your local `.env`

Make a copy of `.env.example` and name the copy:

```text
.env
```

Your project should now contain:

```text
.env
.env.example
```

### Step 2 — Edit `.env`

Open `.env` and replace the placeholder values with your **actual local values**.

For example:

```env
SECRET_KEY=your-real-secret-key
DEBUG=True

DATABASE_NAME=myecomdb
DATABASE_USER=root
DATABASE_PASSWORD=your-real-mysql-password
DATABASE_HOST=localhost
DATABASE_PORT=3306

EMAIL_HOST_USER=your-real-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password

RAPIDAPI_KEY=your-real-rapidapi-key
```

### ⚠️ Very important

**Never put your real passwords, API keys, or secret keys inside `.env.example`.**

Use:

```text
.env.example → placeholder values
.env         → your real local values
```

And **never upload `.env` to GitHub**.

Your `.gitignore` should contain:

```text
.env
```

---

# 5️⃣ Configure MySQL 🗄️

Make sure your MySQL server is installed and running.

The local configuration normally looks like:

```text
Host: localhost
Port: 3306
```

Create the database specified in your `.env`.

For example, if you have:

```env
DATABASE_NAME=myecomdb
```

create:

```sql
CREATE DATABASE myecomdb;
```

Make sure the database username and password in `.env` are correct.

---

# 6️⃣ Run Database Migrations

Django uses migrations to create the required database tables.

Run:

```bash
python manage.py migrate
```

Wait for the command to finish successfully.

---

# 7️⃣ Check the Django Project

Before starting the website, run:

```bash
python manage.py check
```

If everything is configured correctly, you should see:

```text
System check identified no issues (0 silenced).
```

---

# 8️⃣ Create an Admin Account 👤

If you want to use the Django admin panel, create an administrator account:

```bash
python manage.py createsuperuser
```

Follow the instructions shown in the terminal.

---

# 9️⃣ Start the Website ▶️

Start the Django development server:

```bash
python manage.py runserver
```

You should see:

```text
Starting development server at http://127.0.0.1:8000/
```

---

# 🌐 1️⃣0️⃣ Open the Website

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

🎉 Your E-commerce Website is now running locally.

---

# 🛑 Stop the Server

To stop the Django server, go back to the terminal and press:

```text
CTRL + C
```

---

# 🔄 Run the Project Again Later

Once the project has already been installed and configured, you don't need to repeat the complete setup.

Open Command Prompt and run:

```bash
cd EcommercePythonapp
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

Start Django:

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

---

# ⚡ Quick Command List

For a project that has already been configured:

```bash
cd EcommercePythonapp
venv\Scripts\activate
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

---

# 🔧 Useful Django Commands

### Check project configuration

```bash
python manage.py check
```

### Install project packages

```bash
pip install -r requirements.txt
```

### Apply database migrations

```bash
python manage.py migrate
```

### Create admin user

```bash
python manage.py createsuperuser
```

### Start the development server

```bash
python manage.py runserver
```

### Stop the server

```text
CTRL + C
```

---

# 🔐 Security Reminder

Never commit or upload your real `.env` file.

### ✅ Safe to upload

```text
.env.example
```

with placeholder values such as:

```env
DATABASE_PASSWORD=replace-with-your-password
```

### ❌ Never upload

```text
.env
```

containing real values such as:

```env
DATABASE_PASSWORD=MyRealPassword123
EMAIL_HOST_PASSWORD=MyRealAppPassword
RAPIDAPI_KEY=MyRealApiKey
```

Keep your real credentials only in your local `.env` file.

---

# 🎯 Final Result

After completing the setup:

```text
GitHub
   │
   │ git clone
   ▼
EcommercePythonapp
   │
   ├── .env.example     ← Safe template
   ├── .env             ← Your private local settings
   ├── requirements.txt
   ├── manage.py
   ├── Eshop/
   └── store/
   │
   ▼
Python Virtual Environment
   │
   ▼
Django
   │
   ▼
http://127.0.0.1:8000/
   │
   ▼
🛒 E-commerce Website
```

## ✅ Setup Complete

If you can open:

```text
http://127.0.0.1:8000/
```

and see the E-commerce Website, your local setup is complete. 🎉
