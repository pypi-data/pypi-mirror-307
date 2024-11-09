# setup.py
from setuptools import setup, find_packages

setup(
    name="dynamicDQNet",
    version="0.3.0",
    description="An implementation for dynamic path optimization with DQN network",
    author="dynamicdqnet",
    author_email="18754698764@qq.com",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
