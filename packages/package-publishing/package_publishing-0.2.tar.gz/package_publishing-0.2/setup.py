from setuptools import setup, find_packages

setup(
    name="package_publishing",
    version="0.2",
    packages=find_packages(),
    install_requires=[],
    author="Leonardo",
    author_email="leonardo.h@zerak.at",
    description="A simple example private package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ],
    python_requires='>=3.10',
)