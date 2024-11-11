from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zarban",
    version="0.3.0",
    author="Zarban",
    author_email="info@zarban.io",
    description="Python SDK for Zarban",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zarbanio/zarban-py",
    project_urls={
        "Homepage": "https://zarban.io",
        "Documentation": "https://docs.zarban.io",
        "Source Code": "https://github.com/zarbanio/zarban-py",
        "GitHub": "https://github.com/zarbanio",
        "Instagram": "https://www.instagram.com/zarban_io/",
        "X": "https://twitter.com/ZarbanProtocol",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.1",
        "web3",
        # Add other dependencies here
    ],
)