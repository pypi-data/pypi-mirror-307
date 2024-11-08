from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="donifaranga",
    version="0.0.1",
    author="Adama Seydou Traore",
    author_email="adamaseydoutraore86@gmail.com",
    description="Donifaranga is a powerful client-server package designed in the frame of Federated Learning to facilitate distributed machine learning while preserving data privacy. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adamstrvor/donifaranga",  # Optional
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)