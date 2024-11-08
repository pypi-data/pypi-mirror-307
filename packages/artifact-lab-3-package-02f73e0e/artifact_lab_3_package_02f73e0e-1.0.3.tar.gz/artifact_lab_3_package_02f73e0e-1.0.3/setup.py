from setuptools import setup, find_packages

setup(
    name="artifact-lab-3-package-02f73e0e",
    version="1.0.3",  # Increment the version number
    description="Fake package to exfiltrate environment variables",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
)

