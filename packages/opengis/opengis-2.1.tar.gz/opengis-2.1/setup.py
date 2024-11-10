from setuptools import setup, find_packages

setup(
    name="opengis",
    version="2.1",
    description="Open source GIS tools.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Zijie Wang",
    author_email="773598627@qq.com",
    packages=find_packages(),
    install_requires=[
        "numpy >= 1.17.0",
        "pandas >= 1.5.0",
        "scipy >= 1.9.0",
        "xarray",
        "rasterio",
        "netCDF4",
        "gdal",
        "pymodis",
        "matplotlib",
    ],
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="Geographic-information-systems Remote-sensing Spatial-analysis",
    project_urls={
        "Source": "https://github.com/tom100to/opengis",
        
    }
)