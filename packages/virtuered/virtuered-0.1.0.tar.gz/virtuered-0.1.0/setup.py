from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    "requests>=2.25.1",
    "rich>=10.0.0"
]

setup(
    name="virtuered",
    version="0.1.0",
    author="Virtue AI",
    author_email="yijiazheng@virtueai.com",
    license="MIT",
    description="CLI tool for VirtueAI VirtueRed",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Virtue-AI/VirtueRed-CLI.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'virtuered=virtuered.cli:main',
        ],
    },
)