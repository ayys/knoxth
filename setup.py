import os
from distutils.core import setup

from setuptools import find_packages

# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, "README.md"), encoding="utf-8") as f:
        long_description = f.read()
except Exception:
    long_description = ""

print(find_packages(exclude=["knoxth_project", "test_app", "test_app.migrations"]))

setup(
    # Name of the package
    name="knoxth",
    # Packages to include into the distribution
    packages=find_packages(exclude=["knoxth_project", "test_app", "test_app.migrations"]),
    # Start with a small number and increase it with
    # every change you make https://semver.org
    version="0.0.3",
    # Chose a license from here: https: //
    # help.github.com / articles / licensing - a -
    # repository. For example: MIT
    license="GPL-3.0",
    # Short description of your library
    description="Knoxth uses Knox tokens to provide token-level authorization management for DRF viewsets",
    # Long description of your library
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Your name
    author="Ayush Jha",
    # Your email
    author_email="ayushjha@protonmail.com",
    # Either the link to your github or to your website
    url="https://gitlab.com/ayys",
    # Link from which the project can be downloaded
    download_url="",
    # List of keywords
    keywords=[
        "drf",
        "authorization",
        "tokenauthorization",
        "knox",
        "scope",
    ],
    # List of packages to install with this one
    install_requires=[
        "knox",
        "djangorestframework",
        "django>=2.2",
        "jinja2",
        "boto3",
    ],
    # https://pypi.org/classifiers/
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Session",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
    ],
)
