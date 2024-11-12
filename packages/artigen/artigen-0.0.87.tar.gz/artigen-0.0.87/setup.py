from setuptools import setup, find_packages

setup(
    name="artigen",
    version="0.0.87",
    author="Dev Attentions",
    author_email="dev@attentions.ai",
    maintainer="sharky_19",
    maintainer_email="suraj.singh@attentions.ai",
    description="A small example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Homepage": "https://github.com/pypa/sampleproject",
        "Issues": "https://github.com/pypa/sampleproject/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
