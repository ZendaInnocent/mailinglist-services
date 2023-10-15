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

The project will be available at localhost:8000
