#!/usr/bin/env python3
"""Setup script for Thirsty's Game Studio Agent System."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
requirements_file = this_directory / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file) as f:
        requirements = [line.strip() for line in f 
                       if line.strip() and not line.startswith('#')]

setup(
    name="thirstys-game-studio-agent",
    version="0.1.0",
    author="Thirsty's Game Studio",
    author_email="",
    description="Multi-agent orchestration system for game development community insights",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IAmSoThirsty/Thirstys_Game-Studio",
    packages=find_packages(exclude=["tests", "tests.*", "android", "cpp", "dotnet", "web"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'pytest-asyncio>=0.21.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
        'full': [
            'praw>=7.7.1',
            'discord.py>=2.3.2',
            'requests>=2.31.0',
            'textblob>=0.17.1',
            'spacy>=3.7.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'thirsty-agent=agent.runner:main',
        ],
    },
)
