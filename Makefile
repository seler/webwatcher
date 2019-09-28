runserver:
	python manage.py runserver

runworker:
	celery -A webwatcher.celery worker -l info -E --pidfile=

runbeat:
	celery -A webwatcher.celery beat -l info --pidfile= --scheduler django_celery_beat.schedulers:DatabaseScheduler

migrate:
	python manage.py migrate

shell:
	python manage.py shell

black:
	black webwatcher

flake8:
	flake8 webwatcher

isort:
	isort -rc webwatcher

mypy:
	mypy -p webwatcher --check-untyped-defs

lint: isort black flake8 mypy

test:
	py.test --pyargs webwatcher --cov=webwatcher --cov-branch --no-cov-on-fail --cov-report=html --cov-report=term:skip-covered -vv --cov-fail-under 100

check: lint test
	@echo "`tput setaf 2`\nAll checks passed. Great success! 🤘\n`tput sgr0`"
