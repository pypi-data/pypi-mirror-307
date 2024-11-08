from setuptools import setup, find_packages

setup(
    name="eztextutils",
    version="0.1.0",
    description="A simple utility package for text operations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Abhay",
    author_email="abhay007official@gmail.com",
    url="https://github.com/aabhay007/eztextutils",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
