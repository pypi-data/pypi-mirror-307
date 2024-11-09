from setuptools import setup, find_packages

setup(
    name="graph_split",      # Replace with your package name
    version="0.2.3",               # Initial version
    author="Nure Tasnina",
    author_email="tasnina@vt.edu",
    description="A package to split edges of graph using different crieteria compatible for machine learning model training.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Murali-group/graph-split",  # Your repository
    packages=find_packages(),       # Automatically finds packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)