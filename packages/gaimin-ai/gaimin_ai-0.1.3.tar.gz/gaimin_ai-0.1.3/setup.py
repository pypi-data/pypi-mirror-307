from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gaimin_ai",
    version="0.1.3",
    author="GAIMIN AI",
    author_email="",
    description="A Python client for GAIMIN AI API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gaimin-io-Limited/ai-gaiminapi-package-python",
    packages=find_packages(),
    license="BSD-3-Clause",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.6",
    install_requires=[
        "httpx"
        "pydantic"
    ],
)