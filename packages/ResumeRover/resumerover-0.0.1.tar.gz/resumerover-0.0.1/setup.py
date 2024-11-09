from setuptools import setup, find_packages

setup(
    name='ResumeRover',  # Package name in lowercase
    version='1.0.0',
    packages=find_packages(where='.'),  # Automatically find packages
    install_requires=[
        'PyQt6',
        'beautifulsoup4',
        'extract-emails',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'resumerover=src.main:main',  # Adjust based on your actual structure
        ],
    },
    author='Siyamak Abasnezhad',
    author_email='pydevcasts@gmail.com',
    description='This project is a tool that extracts email addresses from a list of provided website links. Users can input multiple URLs, and the tool will scrape the pages to gather any email addresses found. Additionally, it allows users to send resumes to the extracted emails directly from the application.',
    url='https://github.com/pydevcasts/ResumeRover',  # Your GitHub URL
)