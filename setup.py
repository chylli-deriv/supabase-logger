"""
Setup script for the supabase-logger package.
"""

from setuptools import setup, find_packages
import os

# Read the contents of README.md file
with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="supabase-logger",
    version="0.1.0",
    description="A package for logging AI bot responses to Supabase",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Deriv.com",
    author_email="support@deriv.com",
    url="https://github.com/binary-com/supabase-logger",
    packages=["supabase_logger"],
    package_dir={"supabase_logger": "."},
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
