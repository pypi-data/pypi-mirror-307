from setuptools import setup, find_packages

setup(
    name="zipinfo",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    description="A package to find metadata about zip files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="r0uted",
    author_email="midway-bins-0u@icloud.com",
    url="https://github.com/r0uted/zipinfo",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
