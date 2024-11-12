from setuptools import setup, find_packages

setup(
    name="ml_web_inference",
    version="0.1.0",
    description="A Python package for ML web inference using FastAPI",
    author="xcc",
    author_email="2867389537@qq.com",
    url="https://github.com/xcczach/ml-web-inference",
    packages=find_packages(),
    python_requires=">=3.9,<4",
    install_requires=[
        "fastapi~=0.115.2",
        "uvicorn~=0.31.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    keywords="machine learning, web inference, fastapi, uvicorn",
)
