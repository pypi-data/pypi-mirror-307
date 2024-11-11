# setup.py

from setuptools import setup, find_packages

setup(
    name="my_chroma_helper",                 # The name of your library
    version="0.1.0",                         # Initial version number
    author="Amitav",
    author_email="samit.rkl@gmail.com",
    description="A helper library for Chroma database operations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/amitwangdu/my_chroma_helper",  # Link to your project repo
    packages=find_packages(),                # Automatically finds packages in your library
    install_requires=[
        "chromadb"                           # List dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
     python_requires=">=3.10.0, <4",
)
