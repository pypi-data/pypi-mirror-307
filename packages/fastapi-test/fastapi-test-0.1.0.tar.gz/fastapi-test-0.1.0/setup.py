from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fastapi-test",
    version="0.1.0",
    author="Basel",
    description="A test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={"fastapi_quickstart": ["templates/*"]},
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "fastapi-quickstart=fastapi_quickstart.main:main",
        ],
    },
)