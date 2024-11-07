from setuptools import setup, find_packages

setup(
    name="AIscientists",
    version="0.1.0",
    description="AIscientists package for automated data science workflow.",
    author="AI Scientists",
    author_email="support@AIscientists.ai",
    packages=find_packages(where='.'),  # Updated to find packages in current directory
    package_dir={'': '.'},  # Use the current directory as the package directory
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
