from setuptools import setup, find_packages

setup(
    name="pylogicalprogram",
    version="1.4",
    author="rdinesh808",
    author_email="rdinesh808@gmail.com",
    description="A collection of logical and pattern programs in Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rdinesh808/pylogicalprograms",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["psutil"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
