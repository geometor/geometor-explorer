import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geometor-explorer",
    version="0.0.1",
    author="phi ARCHITECT",
    author_email="phi@geometor.com",
    description="model, render & analyze complex geometric constructions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://geometor.github.io/geomentor-explorer",
    project_urls={
        "COde": "https://github.com/geometor/geometor-explorer",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.9",
)
