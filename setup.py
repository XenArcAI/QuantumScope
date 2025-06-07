"""Setup configuration for QuantumScope PyPI package"""

from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="QuantumScope",
    version="1.0.2",  # Keep in sync with main.py __version__
    author="Parvesh Rawal",
    author_email="team@xenarcai.com",
    description="AI-Powered Research Platform - Advanced CLI tool for intelligent research and report generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xenarcai/QuantumScope",
    project_urls={
        "Bug Reports": "https://github.com/xenarcai/QuantumScope/issues",
        "Source": "https://github.com/xenarcai/QuantumScope",
        "Documentation": "https://github.com/xenarcai/QuantumScope#readme",
        "Changelog": "https://github.com/xenarcai/QuantumScope/releases",
    },
    packages=find_packages(exclude=['tests*']),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.18.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.910",
            "pre-commit>=2.15.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
            "sphinx-autodoc-typehints>=1.12",
        ],
    },
    entry_points={
        "console_scripts": [
            "QuantumScope=QuantumScope.main:main",
        ],
    },
    keywords=[
        "ai", "research", "search", "cli", "artificial-intelligence",
        "websocket", "automation", "report-generation", "data-analysis",
        "intelligence", "academic", "professional", "async", "real-time",
        "machine-learning", "natural-language-processing",
        "scientific-computing", "deep-learning", "knowledge-graph"
    ],
    package_data={
        "QuantumScope": [
            "config/*.json",
            "templates/*.txt",
            "assets/*",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    platforms=["any"],
    license="MIT",
    license_files=["LICENSE"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Text Processing :: General",
        "Topic :: Utilities",
        "Environment :: Console",
        "Natural Language :: English",
    ],
)