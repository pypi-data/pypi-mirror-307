from setuptools import setup, find_packages

setup(
    name="izmiran",
    version="0.1.2",
    description=
    "IZMIRAN module for common tasks",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
