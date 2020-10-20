# blog
Blog site

Site has base functionality with login, follow, following users

Site created in python3.8.2, framework-Django, bootstrap

API run in docker container + PostgreSQL database run in another container and launched with docker-compose

If you want run project on your machine you must: 
1. Clone this repository

2. Create and add file .env with your credentials in main directory
- DB_ENGINE=django.db.backends.postgresql
- DB_TYPE=postgres
- DB_DATABASE_NAME=your_database_name  
- DB_USERNAME=your_database_username 
- DB_PASSWORD=your_database_password
- DB_HOST=db
- DB_PORT=5432

4. Create and add file .env-db with your credentials in main directory
- POSTGRES_DB=your_database_name 
- POSTGRES_USER=your_database_username 
- POSTGRES_PASSWORD=your_database_password

3. Run command
- docker-compose run web python manage.py migrate

4. Run command
- docker-compose up --build

