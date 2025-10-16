"""Setup script for Prometheus terminal assistant."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="prometheus-terminal",
    version="1.0.0",
    author="Prometheus Development Team",
    description="An AI-powered terminal assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roywalk3r/prometheus",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: System :: Shells",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "rich>=13.7.0",
        "prompt-toolkit>=3.0.43",
        "pyyaml>=6.0.1",
    ],
    entry_points={
        "console_scripts": [
            "prometheus=main:main",
        ],
    },
)
