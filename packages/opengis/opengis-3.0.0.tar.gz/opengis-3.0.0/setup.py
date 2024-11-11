from setuptools import setup, find_packages

# Runtime Requirements
inst_reqs = [
        "gdal",
        "numpy",
        "xarray",
        "rasterio",
        "netCDF4",
        "pymodis",
]

setup(
    name="opengis",
    version="3.0.0",
    description="Open source GIS tools.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Zijie Wang",
    author_email="773598627@qq.com",
    packages=find_packages(),
    install_requires=inst_reqs,
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="GIS Remote-sensing",
    project_urls={
        "Source":"https://github.com/caaszj/opengis",
        "Tracker":"https://github.com/caaszj/opengis/issues"
        }
)