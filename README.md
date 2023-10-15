# Run the project locally

## Pre-requisite
- Python
- Pipenv
- Git

### Fork the project and clone it locally.
```
git clone https://github.com/ZendaInnocent/mailing-services
cd mailing-services
```

### Create virtual environment and activate it
```
python -m venv .venv
.venv/scripts/activate  # windows
source .venv/bin/activate # linux, macos
```

### Install the dependencies
```
pipenv sync

# Project also use pre-commit, make sure to run
pre-commit install
```

### Set environmental variables

Copy `.env_sample` to `.env` and fill the enviromental variables accordingly.

```
cp .env_sample .env
```

### Create superuser
```
python manage.py createsuperuser
```

### Run the project
```
python manage.py runserver
```

The project will be available at localhost:8000.

Start a Celery worker for tasks
```
celery -A config.celery worker -l info
```

If you are using WSL, you may come accross the error.
```
consumer: Cannot connect to redis://localhost:6379/0: Error 111 connecting to localhost:6379. Connection refused..
```

Make sure you have Redis installed. Check a command for your distro
```
sudo apt install redis-server

# Start the server
sudo service redis-server start
```

If you want to autostart the service (run the service when a WSL distribution starts), create or edit `/etc/wsl.conf` file.
```
[boot]
command="service redis-server start"
```

if you have multipe services to start, separate commands using `;`.
