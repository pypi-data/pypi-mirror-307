from setuptools import setup, find_packages

setup(
    name="rhoGPT-PySDK",
    version="0.1.0",
    author="Rohan",  # Replace with your name or organization
    description="A Python SDK for interacting with the rhoGPT API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Ocean-Moist/rhoGPT-PySDK",  # Update with your repository link
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["requests"],  # Add other dependencies here
    python_requires=">=3.7",
)
