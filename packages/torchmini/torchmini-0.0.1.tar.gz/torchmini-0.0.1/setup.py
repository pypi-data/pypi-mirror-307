from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="torchmini",  
    version="0.0.1",  
    author="Asif Azad",  
    author_email="asifazad0178@gmail.com", 
    description="A simplified PyTorch clone for educational purposes",  
    long_description=long_description,  
    long_description_content_type="text/markdown",  
    url="https://github.com/BRAINIAC2677/torchmini",  
    project_urls={
        "Bug Tracker": "https://github.com/BRAINIAC2677/torchmini/issues",  # Optional issue tracker link
    },
    classifiers=[  
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),  # Automatically discover and include all packages in the project
    install_requires=[  # Required dependencies
        "numpy",  
    ],
    python_requires=">=3.6",  # Minimum Python version required
)
