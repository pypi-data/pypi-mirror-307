from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="news-watch",
    version="0.1.6",
    author="Okky Mabruri",
    author_email="okkymbrur@gmail.com",
    description="A scraper for Indonesian news websites.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/okkymabruri/news-watch",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.10.10",
        "beautifulsoup4>=4.12.3",
        "dateparser>=1.2.0",
        "requests>=2.32.3",
    ],
    entry_points={
        "console_scripts": [
            "newswatch=newswatch.cli:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
