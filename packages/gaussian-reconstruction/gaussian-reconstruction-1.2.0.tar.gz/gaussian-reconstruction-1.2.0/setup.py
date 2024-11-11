from setuptools import setup

packages = ['gsrecon']
requires = [
    "opencv-python",
    "pycolmap"
]

setup(name='gaussian-reconstruction',
	version='1.2.0',
	author='BerryChen',
    description="3D gaussian splatting recosntruction",
    packages=packages,
    package_dir={'requests': 'requests'},
    install_requires=requires,
    include_package_data=True,
)