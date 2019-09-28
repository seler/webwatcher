# webwatcher

Rewrite of [Any2Feed](https://bitbucket.org/seler/any2feed)

development:

    $ pipfile install
    $ docker-compose up postgres rabbitmq celearybeat
    $ python manage.py migrate
    $ python manage.py createsuperuser
    $ python manage.py runserver

