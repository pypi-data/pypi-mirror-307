from setuptools import setup, find_packages

setup(
    name="FD_codepy",           # Project name
    version="0.1.0",                   # Initial version
    description="Codebook and flexibility distance solutions for energy time series analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Rui Yuan",
    author_email="123abcyuanrui@gmail.com",
    url="https://github.com/yourusername/FD_codepy",  # Optional
    packages=find_packages(),          # Automatically find packages in subfolders
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=["numpy",
        "pandas",
        "plotly",
        "tslearn",
        "statsmodels",
        "stumpy",
        "numba"
        ],               # List of dependencies if any
)
