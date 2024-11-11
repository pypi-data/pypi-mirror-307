from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="your-unique-simple-framework",
    version="0.1.2",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple web framework for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/simple-framework",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "Jinja2>=3.0.0",
        "watchdog>=2.1.0",
    ],
) 