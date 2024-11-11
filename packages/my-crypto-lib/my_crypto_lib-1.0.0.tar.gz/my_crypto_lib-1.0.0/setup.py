from setuptools import setup, find_packages

setup(
    name="my_crypto_lib",
    version="1.0.0",
    author="Nitish",
    author_email="nitishnaik2022@gmail.com",
    description="A Python library for encryption and decryption using AES, DES, RSA, and other ciphers",
    long_description="This library provides tools for encrypting and decrypting data using popular cryptographic algorithms like AES, DES, RSA, and more.",
    long_description_content_type="text/markdown",
    url="https://github.com/Nitish-Naik/CNT.git",
    packages=find_packages(),
    install_requires=[
        "pycryptodome>=3.10.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
    ],
    python_requires='>=3.6',
)
