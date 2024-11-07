import setuptools
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


def read_requirements(path):
    if not isinstance(path, list):
        path = [path]
    requirements = []
    for p in path:
        with open(p) as fh:
            requirements.extend([line.strip() for line in fh])
    return requirements


setuptools.setup(
    name="smart_reid",
    version="0.1.3",
    author="Roboflow",
    author_email="help@roboflow.com",
    description="With no prior knowledge of machine learning or device-specific deployment, you can deploy a computer vision model to a range of devices and environments using Roboflow Inference CLI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roboflow/inference",
    packages=find_packages(
        where="./",
        exclude=(
            "examples",
        ),
    ),

    install_requires=read_requirements([
        "requirements.txt",
    ]),
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Typing :: Typed",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8,<=3.12",
)