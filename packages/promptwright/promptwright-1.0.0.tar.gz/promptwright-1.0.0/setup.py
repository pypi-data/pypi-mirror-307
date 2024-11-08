from setuptools import find_packages, setup

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="promptwright",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "certifi>=2023.7.22,<2024.0.0",  # Updated to be compatible with litellm
        "charset-normalizer==3.4.0",
        "idna==3.10",
        "requests==2.32.3",
        "tqdm==4.66.5",
        "urllib3==2.2.3",
        "huggingface-hub==0.26.0",
        "datasets==3.0.2",
        "litellm==1.7.12",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "requests-mock>=1.9.3",
            "mock>=4.0.0",
            "ruff>=0.0.0",
            "datasets==3.0.2",
        ],
    },
    author="Luke Hinds",
    author_email="luke@stacklok.com",
    description="LLM based Synthetic Data Generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StacklokLabs/promptwright",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
