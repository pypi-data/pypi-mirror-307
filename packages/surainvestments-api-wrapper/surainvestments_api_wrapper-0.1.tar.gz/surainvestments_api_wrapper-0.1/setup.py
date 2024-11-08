from setuptools import setup, find_packages

setup(
    name="surainvestments_api_wrapper",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    description="A Python wrapper for the Sura Uruguay Investment API",
    author="Pablo Alaniz",
    author_email="pablo@culturainteractiva.com",
    url="https://github.com/PabloAlaniz/Sura-Investments-API-Wrapper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
