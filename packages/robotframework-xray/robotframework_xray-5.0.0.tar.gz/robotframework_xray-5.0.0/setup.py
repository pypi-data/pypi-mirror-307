from os.path import abspath, dirname, join
from setuptools import setup, find_packages

with open(join(dirname(abspath(__file__)), 'requirements.txt'), encoding='utf-8') as f:
    REQUIREMENTS = f.read().splitlines()

setup(
    name = 'robotframework-xray',
    version = '5.0.0',
    author = 'Cleverson Sampaio',
    author_email = 'cleverson@sampaio.dev.br',
    url = 'https://github.com/kriffx/robotframework-xray',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = REQUIREMENTS,
)