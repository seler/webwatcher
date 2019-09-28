#!/usr/bin/env python3

from setuptools import setup

setup(
    name="WebWatcher",
    version="0.1dev",
    packages=["webwatcher"],
    python_requires=">=3.7",
    install_requires=[
        "django",
        "celery",
        "django-celery-results",
        "django-celery-beat",
        "requests",
        "lxml",
        "feedparser",
        "dateparser",
    ],
)
