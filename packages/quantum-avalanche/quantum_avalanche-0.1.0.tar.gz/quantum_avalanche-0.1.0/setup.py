from setuptools import setup, find_packages

setup(
    name="quantum-avalanche",
    version="0.1.0",
    author="GLIDE",
    author_email="clehackweb@gmail.com",
    description="A custom 256-bit hashing algorithm: QuantumAvalanche_256",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/glidespace/quantum-avalanche",  # Replace with your actual GitHub repo
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
