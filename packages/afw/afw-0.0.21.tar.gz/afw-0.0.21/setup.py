from setuptools import setup, find_packages
from os import path, getenv,  system, getcwd


# Read the tag name from an environment variable
tag_name = getenv('TAG_NAME', '0.0.1')  # Default to '0.0.1' if TAG_NAME is not set

# Get the long description from the README file
working_directory = path.abspath(path.dirname(__file__))

# Read the README file
with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# # Set executable permission for infra/create_tests_suite.sh
# system('chmod +x infra/create_tests_suite.sh')


# # Run the create_tests_suite.sh script with the new folder name argument
# new_folder_name = "e2e_tests"  # Replace with the desired folder name

# system(f'./infra/create_tests_suite.sh {new_folder_name}')

setup(
    name='afw', # Required
    version=tag_name, #'0.0.18', # Required - update version number when new code is entered
    url='https://github.com/tsachikotek/AFW',
    author='Tsachi Kotek',
    author_email='tsachikotek@gmail.com',
    description='-',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=requirements,
)