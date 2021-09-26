import os

from setuptools import setup

requirements_files = ["requirements.txt", "service/service_requirements.txt"]

setup_dir = os.path.dirname(os.path.abspath(__file__))

requirements = []

for file_name in requirements_files:
    with open(os.path.join(setup_dir, file_name), "r") as req_file:
        requirements += [line.strip() for line in req_file if line.strip()]

setup(
    name="urlclassifier",
    version="0.1.0",
    packages=["urlclassifier"],
    install_requires=requirements,
)
