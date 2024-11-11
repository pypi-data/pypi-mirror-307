# setup.py

from setuptools import setup, find_packages

setup(
    name='bisHash',
    version='1.0.4',
    packages=find_packages(),
    description='A simple hashing algorithm library',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author='Group',
    author_email='your.email@example.com',
    url='https://github.com/michaelIldefonso/Hashing-Algorithm',
    python_requires='>=3.6',
    install_requires=[            # List your dependencies here
        "argon2-cffi",
        "ratelimit",
    ],

)
