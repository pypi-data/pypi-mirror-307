# from distutils.core import  setup
from setuptools import setup, find_packages

# packages = ['gaussian-reconstruction']
setup(name='gaussian-reconstruction',
	version='1.2',
	author='BerryChen',
    packages=find_packages(),
    package_dir={'requests': 'requests'},)