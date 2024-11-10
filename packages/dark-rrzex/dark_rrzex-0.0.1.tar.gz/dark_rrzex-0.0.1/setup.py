import setuptools
with open("README.md", "r" , encoding="utf-8") as fh:
    lng_description = fh.read()

with open("requirements.txt", "r") as f:
    reqe = f.read().split("\n")
    
setuptools.setup(
    name = "dark-rrzex",
    version = "0.0.1",
    authors = "ALEX",
    author_email="alexcrow221@gmail.com",
    long_description_content_type="text/markdown",
    description = "lib for ai",
    long_description=lng_description,
    python_requires=">=3.6",
    url="https://github.com/A-X-1/test-lib",
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
    install_requires =reqe,
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)