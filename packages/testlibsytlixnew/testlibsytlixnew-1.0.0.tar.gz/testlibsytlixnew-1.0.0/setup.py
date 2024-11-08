from setuptools import setup, find_packages
                    
setup(
name="testlibsytlixnew",
version="1.0.0",
author="LixNew",
author_email="lixnew12@gmail.com",
description="test",
long_description=open("README.md", encoding="utf-8").read(),
long_description_content_type="text/markdown",
packages=find_packages("src"),
package_dir={"": "src"},
classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
],
python_requires=">=3.7",
install_requires=[
],
)