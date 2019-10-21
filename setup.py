import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Nom_Projet""
    version="0.0.1",
    author="Jlaqueyrie",
    author_email="author@example.com",
    description="Example de structure de projet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleprojectl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
