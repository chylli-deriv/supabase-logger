"""
Setup script for the supabase-logger package.
"""

from setuptools import setup, find_packages

setup(
    name="supabase-logger",
    version="0.1.0",
    description="A package for logging AI bot responses to Supabase",
    author="Binary.com",
    packages=["supabase_logger"],
    package_dir={"supabase_logger": "."},
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
