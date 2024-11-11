from setuptools import setup, find_packages

setup(
    name="shieldid",
    version="0.1.4",
    author="Jung JinYoung",
    author_email="bungker@gmail.com",
    description="utilities package for SHIELD ID(Security365 Cloud Idaas)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jyjung/shieldid",
    packages=find_packages(),
    install_requires=[
        "progressbar2",
        "Requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)