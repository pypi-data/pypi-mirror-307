from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pydrolono",
    version="0.1.0",
    author="Paul Skeie",
    author_email="paul.skeie@gmail.com", 
    description="A Python client for accessing hydrological data from NVE's Hydrology API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paulskeie/pydrolono",
    project_urls={
        "Bug Tracker": "https://github.com/paulskeie/pydrolono/issues",
        "Documentation": "https://github.com/paulskeie/pydrolono#readme",
        "Source Code": "https://github.com/paulskeie/pydrolono",
    },
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Hydrology",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
)
