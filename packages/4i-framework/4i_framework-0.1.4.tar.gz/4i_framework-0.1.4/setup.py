from setuptools import setup, find_packages

setup(
    name="4i-framework",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "Jinja2>=3.0.0",
        "watchdog>=2.1.0",
    ],
    package_data={
        'simple_framework': ['*'],
    },
    python_requires='>=3.6',
) 