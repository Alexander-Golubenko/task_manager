# Task Manager API (Django + DRF)

A simple task management REST API built with Django and Django REST Framework.  
It allows you to manage tasks, subtasks, and categories with filtering, searching, and statistics.

## Features

- CRUD for tasks, subtasks, and categories
- Status tracking and deadlines
- Filtering, ordering, and search
- Built-in task statistics endpoint
- Admin panel
- SQLite by default (MySQL optional)

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo.git
cd task_manager
```

### 2. Create virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up environment variables

Copy example `.env` file and replace with your own secret key:

```bash
cp .env.example .env
```

Example content:

```
SECRET_KEY=your-secret-key-here
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## API Endpoints

| Method | Endpoint                  | Description                    |
|--------|---------------------------|--------------------------------|
| GET    | /tasks/                   | List tasks                     |
| POST   | /tasks/                   | Create new task                |
| GET    | /tasks/<id>/              | Get task by ID                 |
| PUT    | /tasks/<id>/              | Update task                    |
| DELETE | /tasks/<id>/              | Delete task                    |
| GET    | /tasks/statistics/        | Summary statistics             |
| GET/POST | /subtasks/              | List or create subtasks        |
| GET/PUT/DELETE | /subtasks/<id>/   | Retrieve, update or delete     |
| GET/POST | /categories/            | List or create categories      |
| GET    | /categories/<id>/count_tasks/ | Task count per category   |

## Tech Stack

- Python 3.13+
- Django 5.2.1
- Django REST Framework
- SQLite3 (default)
- dotenv (.env support)
- django-filter

## Notes

- You can use `pipreqs . --force` to regenerate `requirements.txt` based on actual imports.
- The database file `db.sqlite3` will be created automatically after `migrate`. If you already have it, place it in the project root.
- Admin panel is available at `/admin/` (create superuser with `python manage.py createsuperuser`).