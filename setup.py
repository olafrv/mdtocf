# https://packaging.python.org/guides/distributing-packages-using-setuptools/

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# with open("requirements.txt", "r") as fh:
#    requirements = [line.strip() for line in fh]

with open("VERSION", "r") as fh:
    version = fh.readline()

setuptools.setup(
    name="mdtocf",
    version=version,
    author="Olaf Reitmaier Veracierta",
    author_email="olafrv@gmail.com",
    description="Markdown files/directory publishing to Atlassian Confluence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olafrv/mdtocf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    # install_requires=requirements,
)
