import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="inspiro",
    version="0.0.3",
    author="SamHDev",
    author_email="sam.fucked.up@samh.dev",
    description="Python3 API wrapper for InspiroBot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SamHDev/inspiro",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
