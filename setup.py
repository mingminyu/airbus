from setuptools import setup, find_packages

VERSION = "0.0.3"

setup(
    name='airbus',
    version=VERSION,
    description='airbus package',
    platforms=["all"],
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        "rich==11.2.0"
        ],
    )
