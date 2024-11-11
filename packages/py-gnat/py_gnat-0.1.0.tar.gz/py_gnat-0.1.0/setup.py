from setuptools import setup, find_packages

setup(
    name="py_gnat",
    version="0.1.0",
    author="Zhuoyun Zhong",
    author_email="zzy905954450@gmail.com",
    description="Python implementation of Geometric Near-neighbor Access Tree (GNAT) data structure from OMPL to search nearest neighbors.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ZhuoyunZhong/py_gnat",  # GitHub or project URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
