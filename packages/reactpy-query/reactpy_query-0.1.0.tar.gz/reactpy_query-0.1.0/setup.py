from setuptools import setup, find_packages

setup(
    name="reactpy-query",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "reactpy>=1.0.0",
        "asyncio>=3.4.3"
    ],
)
