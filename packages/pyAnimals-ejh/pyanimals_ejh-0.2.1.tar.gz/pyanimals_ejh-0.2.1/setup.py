from setuptools import setup, find_packages

setup(
    name="pyAnimals_ejh",
    version="0.2.1",
    description="A fun package that displays animals on the terminal with movement and messages.",
    author="Emma Zhu, Haley Hobbs, Jason Tran, Jenna Han",
    author_email="egz2006@nyu.edu, hkh9725@nyu.edu, ht2354@nyu.edu, jh7765@nyu.edu",
    packages=find_packages(),
    install_requires=[],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/software-students-fall2024/3-python-package-ejh",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
