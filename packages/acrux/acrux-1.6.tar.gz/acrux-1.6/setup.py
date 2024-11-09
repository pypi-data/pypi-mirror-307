import requests
from setuptools import setup

PACKAGE_NAME = "acrux"
with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()


def last_version() -> str:
    response = requests.get(f'https://pypi.org/pypi/{PACKAGE_NAME}/json')
    if response.status_code == 200:
        return response.json()['info']['version']
    else:
        return "0.0"


def increment_version(version: str) -> str:
    new_version = int(float(version) * 10) + 1
    return "{0:.1f}".format(new_version / 10)


setup(
    name=PACKAGE_NAME,
    version=increment_version(last_version()),
    description="Simple Exploratory Data Analysis tool.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/darkhan-ai/acrux",
    license="MIT",
    packages=[PACKAGE_NAME],
    install_requires=[
        "pandas",
        "matplotlib",
        "seaborn",
    ],
    zip_safe=False,
)
