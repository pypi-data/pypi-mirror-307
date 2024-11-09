from setuptools import setup, find_packages
from pywaybackup.__version__ import __version__ as VERSION
import sys

import sqlite3
MIN_SQLITE_VERSION = (3, 25, 0)
if sqlite3.sqlite_version_info < MIN_SQLITE_VERSION:
    sys.exit(
        f"SQLite version 3.25 or higher is required. "
        f"Detected version is {sqlite3.sqlite_version}."
    )

import pkg_resources
def parse_requirements(filename):
    with open(filename, 'r') as f:
        requirements = [str(requirement) for requirement in pkg_resources.parse_requirements(f)]
    return requirements

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pywaybackup',
    version=VERSION,
    python_requires='>=3.8',
    packages=find_packages(),
    install_requires=parse_requirements('./requirements.txt'),
    entry_points={
        'console_scripts': [
            'waybackup = pywaybackup.main:main',
        ],
    },
    author='bitdruid',
    author_email='bitdruid@outlook.com',
    description='Download snapshots from the Wayback Machine',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='wayback machine internet archive',
    url='https://github.com/bitdruid/python-wayback-machine-downloader',
)
