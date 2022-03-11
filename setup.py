from setuptools import setup, find_packages

VERSION = "0.0.3"

setup(
    name='airbus',
    version=VERSION,
    description='airbus package',
    platforms=["all"],
    license='GPL',
    author="yumingmin",
    author_email="yu_mingm623@163.com",
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        "rich==11.2.0",
        "rich[jupyter]",
        "click==8.0.4",
        "requests==2.25.1",
        "impyla==0.17.0",
        "pandas==1.4.1"
        # "lazy-object-proxy=1.7.1",
        ],
    )
