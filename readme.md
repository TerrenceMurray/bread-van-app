# Bread Van CLI App

A command-line application built with **Flask CLI** to support the *Bread Van* use cases.  
The system models **Drivers** and **Residents**, with features for scheduling stops, viewing inbox messages, requesting stops, and checking driver status.

---

## 🚀 Features

- **Database Initialization**
  - `flask init` – create and initialize the database.

- **Authentication**
  - `flask auth login --username <username> --password <password>` – login and persist session.
  - `flask auth logout` – logout and clear session.
  - `flask auth whoami` – check current logged-in user.

- **Users**
  - `flask user list [--f string|json]` – list users.

- **Drivers**
  - `flask driver list [--f string|json]` – list drivers (requires driver login).
  - `flask driver schedule <street> <scheduled_date>` – schedule a stop for a street (use case 1, requires driver login).

- **Streets**
  - `flask street list [--f string|json]` – list streets (requires login).

- **Testing**
  - `flask test user unit` – run user unit tests.
  - `flask test user int` – run user integration tests.
  - `flask test user all` – run all tests.

---

## 🛠️ Requirements

- Python 3.10+  
- Flask  
- Click  
- SQLAlchemy  
- pytest  

Install dependencies:
```bash
pip install -r requirements.txt
