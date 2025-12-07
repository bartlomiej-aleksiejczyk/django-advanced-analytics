# Start a new project

django-admin startproject mysite djangotutorial

# Start a new app

python manage.py startapp polls

# Create migration files from model changes

python manage.py makemigrations

# Apply migrations to the database

python manage.py migrate

# Run development server

python manage.py runserver 8080

# Create superuser for admin panel

python manage.py createsuperuser

# Collect static files into STATIC_ROOT (useful for production)

python manage.py collectstatic

# Run a worker

python manage.py qcluster

# Docker console

docker compose exec -it web "sh"

===

# NPM stuff

===

# npm run dev

# npm run build
