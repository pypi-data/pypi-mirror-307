# setup.py
from setuptools import setup, find_packages

setup(
    name="body_composition_analysis",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "nibabel==5.3.2",
        "numpy>=1.18.0, <2.1.0",  # Use compatible range
        "pandas>=1.0",            # Adjust pandas version as needed
        "scipy>=1.5",             # Adjust scipy version as needed
        "setuptools>=40.0.0",     # Use a more general version for setuptools
        "SimpleITK==2.4.0",       # Keep only one SimpleITK version
        "TotalSegmentator==2.4.0"
    ],
    entry_points={
        "console_scripts": [
            "body_composition=body_composition.cli:main"
        ]
    },
    author="Yeseul Kim",
    author_email="ykim23@mdanderson.org",
    description="A package for body composition analysis from DICOM images.",
)

