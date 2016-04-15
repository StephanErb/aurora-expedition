
from setuptools import setup, find_packages


# We would normally pin those in a requirements.txt, but as we abuse github
# as a package repository in this tutorial we resort to pinning those here.
install_requires = [
    'Flask==0.10.1',
    'Gunicorn==19.4.5',
    'itsdangerous==0.24',
    'Jinja2==2.8',
    'MarkupSafe==0.23',
    'Werkzeug==0.11.7'
]

setup(
    name='toyserver',
    description='This is a toy server powered by Flask',
    packages=find_packages(),
    url='https://github.com/StephanErb/aurora-expedition',
    install_requires=install_requires,
    author='Stephan Erb',
    author_email='stephan.erb@blue-yonder.com',
)
