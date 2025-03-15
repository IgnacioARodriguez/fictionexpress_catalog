# Fiction Express - Technical Test

This project is a Django Rest Framework (DRF) API for managing a book catalog, with JWT authentication and role-based access control.

## 📌 Technologies
- Django Rest Framework
- JWT for authentication
- Docker + Docker Compose
- MySQL/MariaDB

## 📌 Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/fictionexpress_catalog.git
     ```
2. Change to the project directory:
    ```bash
    cd fictionexpress_catalog
    ```
3. Create a `.env` file in the project root directory:
    ```bash
    python -m venv venv
    > linux: source venv/bin/activate 
    > windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
4. Run migrations and application:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```
5. Access the API at `http://localhost:8000/`

    