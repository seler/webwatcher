#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name="WebWatcher",
    version="0.1.dev0",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "django",
        "celery",
        "django-celery-results",
        "django-celery-beat",
        "requests",
        "lxml",
        "cssselect",
        "feedparser",
        "dateparser",
    ],
)
