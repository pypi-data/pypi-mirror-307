from setuptools import setup, find_packages

setup(
    name="password-magic",
    version="0.1.0",
    description="A package for generating, validating, and checking the strength of passwords",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Abhay",
    author_email="abhay007official@gmail.com",
    url="https://github.com/aabhay007/password-magic",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
