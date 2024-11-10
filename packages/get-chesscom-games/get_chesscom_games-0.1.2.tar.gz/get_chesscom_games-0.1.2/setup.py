from setuptools import setup, find_packages

setup(
    name="get-chesscom-games",  
    version="0.1.2",  
    description="A Python API Wrapper for Chess.com to fetch chess games", 
    long_description=open('README.md').read(),  
    long_description_content_type="text/markdown",  
    author="PixelatedWins",
    packages=find_packages(),  
    install_requires=[  
        "requests",
    ],
    python_requires='>=3.6',  
)
