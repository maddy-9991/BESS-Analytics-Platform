"""Setup script for BESS Analytics Platform."""

from setuptools import setup, find_packages

setup(
    name="bess-analytics-platform",
    version="1.0.0",
    description="Battery Energy Storage System Analytics Platform",
    author="Hammad Imran",
    author_email="hammadimran100@gmail.com",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn[standard]>=0.27.0",
        "pandas>=2.1.4",
        "numpy>=1.26.3",
        "scikit-learn>=1.3.2",
        "pydantic>=2.5.3",
        "pydantic-settings>=2.1.0",
    ],
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
    ],
)
