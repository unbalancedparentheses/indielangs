"""setup.py controls the build, testing, and distribution of the egg"""

from setuptools import setup, find_packages
import os.path

PROJECT = "indielangs"

def get_requirements():
    """Reads the installation requirements from requirements.txt"""
    with open("requirements.txt") as f:
        return [line.rstrip() for line in f if not line.startswith("#")]


setup(
    name=PROJECT,
    version="0.1",
    description="Store list of languages detected by github in database",
    classifiers=[
        'Programming Language :: Python'
    ],
    keywords='worker',
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
    install_requires=get_requirements()
)
