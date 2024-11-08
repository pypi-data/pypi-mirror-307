from setuptools import setup, find_packages

setup(
    name="SciLite",
    version="0.0.1",
    author="Ayush Jain Sparsh",
    author_email="ayushjainsparsh2004.ajs@gmail.com",
    description="Sci-Lite is Light version of Supervised Machine Learning Model",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",
    packages=find_packages(),
    install_requires=[
        'pandas','scikit-learn','catboost'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
