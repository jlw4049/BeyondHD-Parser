import os

from setuptools import setup

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS",
    "Operating System :: POSIX :: Linux",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

with open(os.path.join(os.path.dirname(__file__), "README.md")) as fd:
    ext_long_desc = fd.read()

setup(
    name="BeyondHD-Parser",
    version="1.0.6",
    description="Tool to search/scrape BeyondHD for torrent information",
    long_description=ext_long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/jlw4049/BeyondHD-Parser",
    author="Jessie Wilson",
    author_email="jessielw4049@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="BeyondHD-Parser",
    packages=["beyondhd_parser"],
    install_requires=["beautifulsoup4", "browser-cookie3", "requests"],
)
