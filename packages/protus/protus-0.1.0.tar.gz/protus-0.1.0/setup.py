from setuptools import setup, find_packages

setup(
    name="protus",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Add any dependencies your SDK needs here, e.g., 'requests'
    ],
    description="Python SDK for Protus (https://protus.dev)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Tomer Gal",
    author_email="tomer@protus.dev",
    url="https://protus.dev",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)
