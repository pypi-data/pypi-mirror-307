from setuptools import setup, find_packages

setup(
    name='file-management-package',  # Make sure this name is unique on PyPI
    version='0.8.1',  # Increment version with each release
    packages=find_packages(),  # Automatically find your package modules

    # Dependencies for your package
    install_requires=[
        'setuptools',
        # Add any other dependencies here
    ],

    # Package author details
    # Package author details
    author='Pascal Benink',
    author_email='2sam2samb+PythonFile@gmail.com',

    # Short description of your package
    description='A package for file management',

    # Long description, often read from a README file
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',  # For Markdown support

    # URL for your package's homepage or GitHub repository
    url='https://github.com/Pascal-Benink/File-Management-Package',

    # Classifiers help users find your package by categorizing it
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Replace with your license
        'Operating System :: OS Independent',
    ],

    # Minimum Python version required for the package
    python_requires='>=3.10.12',
)