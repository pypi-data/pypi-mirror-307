from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="AIscientists",
    version="0.1.1",
    description="AIscientists package for automated data science workflow.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AI Scientists",
    author_email="support@AIscientists.ai",
    packages=find_packages(),
    package_dir={"": "."},
    install_requires=[
        "requests",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "aiscientists-chat=AIscientists.main:get_response"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)