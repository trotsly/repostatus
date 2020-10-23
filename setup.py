#!/usr/bin/env python3
"""Setup RepoStatus"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


req_pkgs = [
    'simber',
    'requests'
]


if __name__ == '__main__':
    setuptools.setup(
        name="repostatus",
        version="0.1.0",
        author="Deepjyoti Barman",
        author_email="deep.barma30@gmail.com",
        description="Repository Status",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/trotsly/repostatus",
        packages=setuptools.find_packages(),
        classifiers=(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        python_requires=">=3.*",
        install_requires=req_pkgs,
        setup_requires=['setuptools'],
    )
