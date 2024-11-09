from setuptools import setup, find_packages

setup(
    name="theodoretools",
    version="0.0.9",
    author="Theodore",
    author_email="your.email@example.com",
    description="A short description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/theodoreniu/theodoretools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "python-dotenv>=1.0.1",
        "streamlit>=1.38.0",
        "qrcode>=7.4.2",
        "streamlit-javascript>=0.1.5",
    ],
)
