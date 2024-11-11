from setuptools import setup, find_packages

setup(
    name="Human_Data_Analytics",                     
    version="0.7.3",
    author = "Cesare Bidini, Nicolò Rinaldi",                              
    packages=find_packages(),
    # install_requires=[                            
    #     "somepackage>=1.0.0",
    # ],
    python_requires=">=3.6",                      
    author_email="your.email@example.com",
    description="A brief description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cesarbid/Human-Data-Analytics",
    classifiers=[                                 
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
