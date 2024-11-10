from setuptools import setup, find_packages

setup(
    name="Rai_modules",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        # "dependance1>=1.0",
    ],
    description="C'est un package python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Raikou 320",
    author_email="duchaussoytheo@outlook.fr",
    url="https://github.com/Raikou320/RaiModules.py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
