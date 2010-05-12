import os
from setuptools import setup, find_packages

from app_metrics import VERSION


f = open(os.path.join(os.path.dirname(__file__), 'README.txt'))
readme = f.read()
f.close()

setup(
    name='django-app-metrics',
    version=".".join(map(str, VERSION)),
    description='django-app-metrics is a reusable Django application for tracking and emailing application metrics.',
    long_description=readme,
    author='Frank Wiles',
    author_email='frank@revsys.com',
    url='http://github.com/frankwiles/django-app-metrics/tree/master',
    packages=find_packages(),
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

