from setuptools import setup, find_packages

setup(
    name="excel_dependency_graph",
    version="0.1.0",
    description="A library to parse Excel formulas and create a dependency graph for cells.",
    author="Jitesh",
    author_email="jpgurav97@gmail.com",
    packages=find_packages(),
    install_requires=[
        "openpyxl>=3.0.0",
        "networkx>=2.5",
        "matplotlib>=3.1.0"
    ],
    entry_points={
        "console_scripts": [
            "excel_dependency_graph=excel_dependency_graph:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
