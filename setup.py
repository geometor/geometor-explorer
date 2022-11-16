import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geometor",
    version="0.0.2",
    author="phi ARCHITECT",
    author_email="phi@geometor.com",
    description="model, render & analyze complex geometric constructions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://geometor.github.io/geometor-explorer",
    project_urls={
        "Code": "https://github.com/geometor/geometor-explorer",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.9",
    install_requires=['sympy', 'matplotlib']
)
