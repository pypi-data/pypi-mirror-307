from setuptools import setup, find_packages

setup(
    name="ytanalysis",  
    version="0.1.0",  
    author="Dinesh Ram",
    author_email="dineshramdsml@gmail.com",
    description="A package for analyzing YouTube channel statistics using the YouTube API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dineshram0212/youtube-analysis", 
    packages=find_packages(),
    install_requires=[
        "google-api-python-client",
        "pandas",
        "seaborn",
        "matplotlib"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
