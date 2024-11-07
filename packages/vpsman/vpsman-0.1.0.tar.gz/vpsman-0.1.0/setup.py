from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vpsman",
    version="0.1.0",
    author="mason_dev",
    author_email="websong16@gmail.com",
    description="A VPS management tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/vpsman",
    packages=find_packages(),
    install_requires=[
        "questionary>=1.10.0"
    ],
    entry_points={
        'console_scripts': [
            'vpsman=vpsman.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)