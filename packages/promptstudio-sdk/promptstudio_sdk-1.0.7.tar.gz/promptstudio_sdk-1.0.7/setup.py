from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="promptstudio-sdk",
    version="1.0.7",
    author="PromptStudio",
    author_email="support@promptstudio.dev",
    description="Python SDK for PromptStudio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/promptstudio/python-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.19.0",
        "aiohttp>=3.8.0",  # For async HTTP requests
        "typing-extensions>=4.0.0",  # For TypedDict support in Python <3.8
    ],
)
