exit()

from setuptools import setup,find_packages
from os import path


here=path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aqua',
    version='0.1',
    packages=find_packages(where='src'),
    url='https://github.com/hui-aqua/hydromodel',
    license='GNU General Public License v3.0',
    author='Hui Cheng',
    author_email='hui.cheng@uis.no',
    description='A simulator for aquaculture structures',
)
