from setuptools import setup, find_packages
from pathlib import Path

# Read the content of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "pypi.md").read_text()

setup(
    name='jadugar',
    version='1.8',  # Update the version number
    packages=find_packages(),
    include_package_data=True,
    package_data={'file': ['../data/*.txt']},
    install_requires=[
        # list your dependencies here
    ],
    author='random',
    description='Jadugar is a fun project for experimentation with Python packages, read more at project links below',
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_urls={ 
        'Documentation': 'https://pypi.org/project/jadugar/',
    },
)
