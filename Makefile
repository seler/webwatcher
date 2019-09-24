run=docker-compose run --rm web

build:
	docker-compose build

migrate:
	$(run) python manage.py migrate

shell:
	$(run) python manage.py shell

bash:
	$(run) bash -i

black:
	$(run) black webwatcher

flake8:
	$(run) flake8 webwatcher

isort:
	$(run) isort -rc webwatcher

mypy:
	$(run) mypy -p webwatcher --check-untyped-defs

lint: isort black flake8 mypy

test:
	$(run) py.test --pyargs webwatcher --cov=webwatcher --cov-branch --no-cov-on-fail --cov-report=html --cov-report=term:skip-covered -vv --cov-fail-under 100

check: lint test
	@echo "`tput setaf 2`\nAll checks passed. Great success! 🤘\n`tput sgr0`"

runserver:
	python manage.py runserver

worker:
	celery -A webwatcher.celery worker -l info

beat:
	celery -A webwatcher.celery beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

