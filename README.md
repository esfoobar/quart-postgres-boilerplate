# Quart Postgres Boilerplate

## Setup
You need to run alembic migrations the first time you run the app. 

To do this, start the app with the following command:
```bash
docker-compose up --build -d
```

Then, run the following command to run the migrations:  
```bash
docker-compose exec web poetry run alembic upgrade head
```
