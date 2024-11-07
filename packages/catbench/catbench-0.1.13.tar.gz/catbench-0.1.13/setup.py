from setuptools import setup, find_packages

setup(
    name="catbench",
    version="0.1.13",
    author="Jinuk Moon",
    author_email="jumooon@snu.ac.kr",
    packages=find_packages(),
    description="MLP benchmarking workflow for catalysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JinukMoon/catbench",
    license="MIT",
    install_requires=[
        "ase>=3.22.1",
        "xlsxwriter>=3.2.0",
        "numpy==1.26",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="MLP benchmarking for catalysis",
    python_requires=">=3.6",
)
