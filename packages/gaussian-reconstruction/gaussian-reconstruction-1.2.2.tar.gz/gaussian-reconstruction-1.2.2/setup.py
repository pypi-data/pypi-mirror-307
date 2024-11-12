from setuptools import setup
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

packages = ['gsrecon']
requires = [
    "opencv-python",
    "pycolmap"
]

setup(name='gaussian-reconstruction',
	version='1.2.2',
	author='BerryChen',
    description="3D gaussian splatting recosntruction",
    packages=packages,
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'requests': 'requests'},
    install_requires=requires,
    include_package_data=True,
)