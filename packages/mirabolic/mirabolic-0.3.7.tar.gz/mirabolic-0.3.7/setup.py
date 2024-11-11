# How to upload to PyPI:
# (1) Change "mirabolic/version" file as you want.
# (2) Clean up any old cruft:
#       rm -rf mirabolic.egg-info dist build
# (2) Make a matching tagged release on GitHub:
#       https://github.com/Mirabolic/mirabolic/releases/new
# (3) Build package
#       python setup.py sdist bdist_wheel
# (4) Upload package
#       twine upload dist/*

import os
import pathlib
from setuptools import setup, find_namespace_packages

# The directory containing this file
this_dir = pathlib.Path(__file__).parent

# The text of the README file
with open(os.path.join(this_dir, "README.md")) as fp:
    README = fp.read()

with open(os.path.join(this_dir, "mirabolic", "version"), mode="r") as fp:
    version = fp.readline().rstrip()

setup(
    name="mirabolic",
    packages=find_namespace_packages(),
    version=version,
    license="MIT",
    description="Statistical and Machine Learning tools from Mirabolic",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Bill Bradley",
    url="https://github.com/Mirabolic/mirabolic",
    # We assume we keep the GitHub tag name consistent with the version
    download_url="https://github.com/Mirabolic/mirabolic/archive/refs/tags/v%s.tar.gz"
    % version,  # noqa: E501
    include_package_data=True,
    package_data={"": ["version"]},
    keywords=["Statistics", "Machine Learning", "CDF", "Quantiles"],
    install_requires=[
        "tensorflow>=2.4.1",
        "numpy>=1.19.2",
        "scipy>=1.8.0",
        "pandas>=1.0.0",
        "matplotlib>=3.5.1",
        "seaborn>=0.11.2",
        "python-dotenv>=1.0.1",
        "openai>=0.51.0",
        "google-generativeai>=0.7.2",
        "huggingface-hub>=0.24.6",
        "requests>=2.32.3",
        "scikit-learn>=1.5.2",
        "umap-learn>=0.5.6",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
