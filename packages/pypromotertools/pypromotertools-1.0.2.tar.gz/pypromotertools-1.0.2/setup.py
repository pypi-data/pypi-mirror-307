import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypromotertools",
    version="1.0.2",
    author="BiomedicalPulsar",
    author_email="biomedicalpulsar@163.com",
    description="a collection of tools for acquiring gene promoters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/biomedicalpulsar/pypromotertools",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['pypromotertools = pypromotertools.pypromotertools:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)