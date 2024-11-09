from setuptools import setup, find_packages

# Read the version from the VERSION file
with open("VERSION") as version_file:
    version = version_file.read().strip()

setup(
    name="SquidLibs",
    version=version,
    author="Squid Coder",
    author_email="squid@squidcoder.com",
    description="A Python library for translation, tkinter Windows, and basic file handling",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SquidCoderIndustries/SquidLibs",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)