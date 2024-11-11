# setup.py
from setuptools import setup, find_packages

setup(
    name='ligoauth',
    version='0.2.6',
    description='ligo upload mac sdk',
    packages=find_packages(where='dist'),
    package_dir={'': 'dist'},
    include_package_data=True,
    python_requires='>=3.6',
)

