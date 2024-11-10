from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() #Gets the long description from Readme file

setup(
    name='ai_sar_2024',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'meta-ai-api',
    ],  # Add a comma here
    author='Shubham',
    author_email='Shub76ham@gmail.com',
    description='Just a simple AI tool for daily simple tasks by Shubham Anand Rashmi - powered by MetaAI',

    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
     project_urls={
           'Source Repository': 'https://github.com/Sm7-git/' #replace with your github source
    }
)
