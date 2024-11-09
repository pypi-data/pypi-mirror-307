from setuptools import setup, find_packages

setup(
    name="steed",
    version="0.1.0",
    description="A drop-in replacement for tee with file buffering and output queue management.",
    author="Ben Skubi",
    author_email="skubi@ohsu.edu",
    packages=find_packages(),
    install_requires=[
        "click",  
    ],
    entry_points={
        "console_scripts": [
            "steed=steed:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
