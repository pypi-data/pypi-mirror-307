from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="gapat",
    version="0.0.1",
    description="A comprehensive framework of GPU-accelerated image reconstruction for photoacoustic computed tomography",
    author="Yibing Wang",
    author_email="ddffwyb@pku.edu.cn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ddffwyb/GAPAT",
    keywords=[
        "photoacoustic computed tomography",
        "large-scale data size",
        "GPU-accelerated method",
        "Taichi Lang for python",
        "multiple GPU platform",
    ],
    packages=find_packages(),
    install_requires=[
        "numpy",
        "taichi==1.2.2",
    ],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
