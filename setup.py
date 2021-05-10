import os
from distutils.core import setup

from setuptools import find_packages

# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
	# Name of the package
	name='knoxth',
	# Packages to include into the distribution
	packages=find_packages('.'),
	# Start with a small number and increase it with
	# every change you make https://semver.org
	version='0.0.1',
	# Chose a license from here: https: //
	# help.github.com / articles / licensing - a -
	# repository. For example: MIT
	license='GPL-3.0',
	# Short description of your library
	description=' Knoxth is an addon for django-rest-knox that lets you do scope based authorization on knox tokens ',
	# Long description of your library
	long_description=long_description,
	long_description_content_type='text/markdown',
	# Your name
	author='Ayush Jha',
	# Your email
	author_email='ayushjha@niyasti.com',
	# Either the link to your github or to your website
	url='https://gitlab.com/ayys',
	# Link from which the project can be downloaded
	download_url='',
	# List of keywords
	keywords=['drf', 'authorization', 'tokenauthorization', 'knox', 'scope'],
	# List of packages to install with this one
	install_requires=[
            ''
        ],
	# https://pypi.org/classifiers/
	classifiers=[]
)