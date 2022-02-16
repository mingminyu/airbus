from setuptools import setup, find_packages

VERSION = "0.0.1"

setup(
    name='airbus',
    version=VERSION,
    description='airbus package',
    platforms=["all"],
    packages=find_packages(),
    zip_safe=False
    )
