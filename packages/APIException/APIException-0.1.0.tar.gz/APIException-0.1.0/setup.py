from setuptools import setup, find_packages

setup(
    name="APIException",
    version="0.1.0",
    author="Ahmet Kutay Ural",
    author_email="ahmetkutayural@gmail.com",
    description="A customizable exception handling library for FastAPI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/akutayural/APIException",  # Replace with your GitHub repo
    packages=find_packages(exclude=["test", "venv"]),
    install_requires=[
        "pydantic>=2.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)