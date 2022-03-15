from setuptools import setup, find_packages

VERSION = "0.0.4"

setup(
    name='airbus',
    version=VERSION,
    description='airbus package',
    platforms=["all"],
    license='GPL',
    author="yumingmin",
    author_email="yu_mingm623@163.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 1 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators"
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Monitoring",
        ],
    install_requires=[
        "rich==11.2.0",
        "rich[jupyter]",
        "click==8.0.4",
        "requests==2.25.1",
        "impyla==0.17.0",
        "pandas==1.4.1",
        "argcomplete==2.0.0",
        "pyppeteer==1.0.2",
        "pyppeteer_stealth==2.7.3",
        # "lazy-object-proxy=1.7.1",
        ],
    entry_points={
        "console_scripts": [
            "airbus=airbus.__main__:main"
            ]
        }
    )
