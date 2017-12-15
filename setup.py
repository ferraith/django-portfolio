"""Setup script for django-portfolio."""
import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-portfolio',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django~=2.0',
        'django-money~=0.12',
    ],
    url='https://github.com/ferraith/django-portfolio',
    license='MIT License',
    author='Andreas Schmidl',
    author_email='ferraith@gmail.com',
    description='Simple Django app to manage a stock portfolio.',
    long_description=README,
    keywords='django finance portfolio stock',
    classifiers=[
        'Development Status :: 1 - Planing',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
