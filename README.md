# core – KanMind Backend

This is a Django REST Framework backend for the KanMind application.

## Features
- User registration, login, and token authentication
- Board, task, and comment management (Kanban style)
- RESTful API endpoints (see API documentation)
- CORS enabled for frontend integration
- Environment variables managed via `.env` and `python-dotenv`

## Setup

1. **Clone the repository and navigate to the project folder:**
   ```powershell
   git clone <your-repo-url>
   cd kanmind_backend
   ```
2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Create a `.env` file** (see `.env.example` if available) and set required environment variables (e.g. `SECRET_KEY`, `DEBUG`, `DATABASE_URL`).
5. **Apply migrations:**
   ```powershell
   python manage.py migrate
   ```
6. **Create a superuser (for admin access):**
   ```powershell
   python manage.py createsuperuser
   ```
7. **Run the development server:**
   ```powershell
   python manage.py runserver
   ```

## API Authentication
- All API endpoints require a valid token in the `Authorization` header:  
  `Authorization: Token <your-token>`
- Obtain a token via registration or login endpoint.

## Testing
- Run all tests with:
  ```powershell
  python manage.py test
  ```

## Admin Interface
- Access the Django admin at `/admin/` with your superuser credentials.

## Notes
- The database file (`db.sqlite3`) and all sensitive files are excluded from version control.
- The backend is separated from the frontend and can be deployed independently.

## Requirements
- Python 3.10+
- Django
- djangorestframework
- python-dotenv

---
For further details, see the API documentation or contact the project maintainer.
