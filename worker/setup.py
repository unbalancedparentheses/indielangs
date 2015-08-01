"""setup.py controls the build, testing, and distribution of the egg"""

from setuptools import setup, find_packages
import os.path

PROJECT = "indielangs"

setup(
    name=PROJECT,
    version="0.1",

    description="Store list of languages detected by github in database",
    keywords='programming languages indie',
    author='Federico Carrone',
    author_email='federico.carrone@gmail.com',
    url='https://github.com/unbalancedparentheses/indielangs',
    license='MIT License',

    packages=find_packages(exclude=['ez_setup']),
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'indielangs = indielangs.worker:main'
        ]
    },
    install_requires=[
        'schedule==0.3.2',
        'PyYAML==3.11',
        'rethinkdb'
    ]
)
