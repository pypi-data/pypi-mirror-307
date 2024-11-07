# setup.py
from setuptools import setup, find_packages

setup(
    name='apacheapi',  # The name of the package
    version='0.2.0',  # Package version
    packages=find_packages(),  # Automatically find all packages (including apache)
    install_requires=[
        'together',  # Add any dependencies required for your package
    ],
    author='Apache Labs',  # Replace with your name
    author_email='your.email@example.com',  # Replace with your email
    description='A Simple Wrapper to allow users to use Athena Finetunes along sinde with LUMIN Finetunes',  # Short description
    long_description=open('README.md').read(),  # Long description from README.md
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/apache',  # Replace with your package's repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
