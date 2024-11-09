# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 08:57:50 2020

@author: HEDI
"""

from setuptools import setup, find_packages
import sys
from os import path

# Chemin du répertoire courant
this_directory = path.abspath(path.dirname(__file__))

# Lecture de la version directement à partir du fichier __version__.py
version_path = path.join(this_directory, 'pymembrane', '__version__.py')
with open(version_path) as f:
    exec(f.read())

# Lire le contenu de votre README.md pour la longue description
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pymembrane',
    version=__version__,
    description='Python library for simulating and optimizing membrane-based food and wastewater treatment processes',
    keywords='wastewater, wastewater treatment, membrane, food process, simulation, optimization',
    author='Hedi ROMDHANA',
    author_email='hedi.romdhana@agroparistech.fr',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ROMDHANA/pymembrane',  # Lien vers votre dépôt GitHub
    license='GPLv3',
    install_requires=[
        'SALib>=1.3.13',
        'CoolProp>=6.4.1',
        'wxPython>=4.1.1',
        'pymoo>=0.4.2.2',
        'tabulate>=0.8.9'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    python_requires='>=3.4',
    packages=find_packages(exclude=['tests', 'docs']),
    package_data={
        'pymembrane': ['*.json', '*.csv', '*.txt']  # Inclure seulement les fichiers pertinents
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pymembrane-help=pymembrane.help_api:list_available_items'
        ],
    }
)
