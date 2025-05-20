from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

with open("VERSION", "r", encoding="utf-8") as fh:
    version = fh.read().strip()

setup(
    name="exemplar-prompt-hub",
    version=version,
    author="Your Name",
    author_email="your.email@example.com",
    description="A modern REST API service for managing and serving AI prompts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shubhanshusingh/exemplar-prompt-hub",
    packages=find_packages(),
    license="MIT",
    license_files=("LICENSE"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "prompt-hub=app.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "app": ["templates/*", "static/*"],
        "": [".env.example"],
    },
) 