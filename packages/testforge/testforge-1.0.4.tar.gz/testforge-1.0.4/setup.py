from setuptools import setup, find_packages

setup(
    name="testforge",
    version="1.0.4",
    packages=find_packages(),
    author_email="support@testforge.ai",
    description="A CLI tool to generate pyton tests using AI.",
    long_description=open("README.md").read(),
    # This tells PyPI to interpret it as Markdown
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/testforge",  # Replace with your GitHub URL

    install_requires=[
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "testforge=testforge.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)
