from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hookme",
    version="0.1.7",
    author="Wadedesignco",
    author_email="hi@wadedev.online",
    description="A powerful webhook handler for Discord and Slack",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wadedesign/hookme",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
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
    ],
) 


# how to upload to pypi
# python3 -m build
# twine upload dist/*

# how to remove dist and build folders
# rm -rf dist build