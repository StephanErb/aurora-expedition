
from setuptools import setup, find_packages

setup(
    name='toyserver',
    description='This is a toy server powered by Flask',
    packages=find_packages(),
    url='https://github.com/StephanErb/aurora-expedition',
    install_requires=['Flask'],
    author='Stephan Erb',
    author_email='stephan.erb@blue-yonder.com',
)
