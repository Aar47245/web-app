This project is a Role-Based Authentication Web Application developed using Python Flask with a REST API backend and a simple Flask-based HTML frontend.
It implements secure JWT-based authentication, role-based access control, and admin-only operations such as creating, deleting, and listing users.
The system includes a default admin account seeded at startup and prevents duplicate registrations.
Students can only access a welcome page, while admins have a dashboard for user management.

frontend/
 ├── app.py
 ├── templates/
 │    ├── login.html
 │    ├── register.html
 │    ├── welcome.html
 │    └── admin.html
 └── static/
