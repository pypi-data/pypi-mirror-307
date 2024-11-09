"""Setup script for the gembatch package."""

import setuptools  # type: ignore

setuptools.setup(
    name="gembatch",
    version="0.0.14",
    description=(
        "A Python library simplifies building language chain applications with Gemini, "
        "leveraging batch mode for cost-effective prompt processing."
    ),
    python_requires=">=3.12",
    author="Benno Lin",
    author_email="blueworrybear@gmail.com",
    packages=setuptools.find_packages(include=["gembatch"]),
    install_requires=[
        "google-cloud-aiplatform>=1.38",
        "firebase-admin>=6.5.0",
        "firebase-functions>=0.4.2",
        "requests>=2.31.0",
    ],
)
