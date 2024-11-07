from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="lianpwn",
    version="1.0.8",
    author="eastXueLian",
    author_email="eastxuelian@gmail.com",
    description="lianpwn based on pwncli",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://eastxuelian.nebuu.la/",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["click", "pwntools", "pwncli"],
    entry_points={"console_scripts": ["lianpwn=lianpwn.cli:cli"]},
)
