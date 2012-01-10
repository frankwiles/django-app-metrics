import os
from setuptools import setup, find_packages

from app_metrics import VERSION


f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()

setup(
    name='django-app-metrics',
    version=".".join(map(str, VERSION)),
    description='django-app-metrics is a reusable Django application for tracking and emailing application metrics.',
    long_description=readme,
    author='Frank Wiles',
    author_email='frank@revsys.com',
    url='https://github.com/frankwiles/django-app-metrics',
    packages=find_packages(),
    package_data={
        'app_metrics': [
            'templates/app_metrics/*',
        ]
    },
    install_requires = [
        'celery',
        'django-celery',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)

