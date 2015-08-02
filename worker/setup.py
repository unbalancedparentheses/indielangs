"""setup.py controls the build, testing, and distribution of the egg"""

from setuptools import setup, find_packages
import os.path

PROJECT = "indielangs"

def get_requirements():
    """Reads the installation requirements from requirements.pip"""
    with open("requirements.txt") as f:
        return [line.rstrip() for line in f if not line.startswith("#")]


setup(
    name=PROJECT,
    version="0.1",
    description="Check list of emails using Rapportive API",
    classifiers=[
        'Programming Language :: Python'
    ],
    keywords='worker',
    author='Federico Carrone',
    author_email='federico.carrone@gmail.com',
    url='https://github.com/jordan-wright/rapportive',
    license='MIT License',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    scripts=[
        'scripts/indielangs',
    ],
    install_requires=get_requirements(),
)
