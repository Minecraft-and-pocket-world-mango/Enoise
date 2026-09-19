from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ENoise",
    version="1.0.1",
    author="Minecraft-and-pocket-world-mango",
    author_email="2929547146@qq.com",
    description="一个轻量级柏林噪声库，支持 Python 3.6.5+",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Minecraft-and-pocket-world-mango/ENoise",
    packages=find_packages(exclude=["tests", "examples"]),
    python_requires=">=3.6.5",
    install_requires=[],
    extras_require={
        "numpy": ["numpy>=1.16"],
        "fast": ["numpy>=1.16"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
)
