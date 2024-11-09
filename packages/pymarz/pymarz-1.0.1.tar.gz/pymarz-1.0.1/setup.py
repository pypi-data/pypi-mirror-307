from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


NAME = "pymarz"
VERSION = "1.0.1"
PYTHON_REQUIRES = ">=3.7"
REQUIRES = [
    "requests",
    "asgiref",
]

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    install_requires=REQUIRES,
    author="SSaeedhoseini",
    author_email="",
    url="https://github.com/SSaeedhoseini/pymarz",
    keywords=["pymarz", "pymarz API", "MarzbanAPI", "Marzban"],
    include_package_data=True,
    long_description_content_type="text/markdown",
    description="Asynchronous Python library for interacting with Marzban",
    long_description=long_description,
    project_urls={
        "Homepage": "https://github.com/SSaeedhoseini/pymarz",
        "Source": "https://github.com/SSaeedhoseini/pymarz",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=PYTHON_REQUIRES,
)
