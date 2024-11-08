# setup.py

from setuptools import setup, find_packages

# Read the contents of README.md for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cloud-composer-json-log-formatter', 
    version='0.1.2',
    author='Anton',
    #author_email='your.email@example.com',  # Replace with your email
    description='A JSON formatter for Composer logging.',  # Short description
    long_description=long_description,  # Long description from README
    long_description_content_type='text/markdown',
    #url='https://github.com/yourusername/json-log-formatter',  # Replace with your repo URL
    packages=find_packages(),  # Automatically find packages in the directory
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Choose your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the Python versions you support
    install_requires=[],  # List dependencies if any
)