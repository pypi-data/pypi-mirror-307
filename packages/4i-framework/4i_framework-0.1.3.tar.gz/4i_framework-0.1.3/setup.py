from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="4i-framework",
    version="0.1.3",
    author="Nishant Maurya",
    author_email="team4ingineers@gmail.com",
    description="A simple web framework for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NISHANTTMAURYA/simple-framework",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "Jinja2>=3.0.0",
        "watchdog>=2.1.0",
    ],
) 