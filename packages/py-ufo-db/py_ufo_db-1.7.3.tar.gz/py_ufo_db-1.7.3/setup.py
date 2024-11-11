import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-ufo-db",  
    version="1.7.3",   
    author="@Sl1dee36, @Atxxxm",
    author_email="spanishiwasc2@gmail.com",
    description="Python Unified Flexible Object Database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SL1dee36/pyufo-db", 
    packages=setuptools.find_packages(),        
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',     
)