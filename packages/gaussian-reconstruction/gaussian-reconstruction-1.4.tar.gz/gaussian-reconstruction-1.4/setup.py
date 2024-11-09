# from distutils.core import  setup
from setuptools import setup

packages = ['gsrecon']
requires = [
    "requests",
]

setup(name='gaussian-reconstruction',
	version='1.4',
	author='BerryChen',
    packages=packages,
    package_dir={'requests': 'requests'},
    install_requires=requires
)