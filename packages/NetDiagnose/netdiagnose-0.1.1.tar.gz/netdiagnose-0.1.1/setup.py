from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="NetDiagnose",  
    version="0.1.1", 
    author="Erwin Pimenta",  
    author_email="erwinpimenta1644@gmail.com", 
    description="A cross-platform network diagnostic tool",  
    long_description=long_description, 
    long_description_content_type="text/markdown",  
    url="https://github.com/gentlsnek/NetDiagnose",  
    packages=find_packages(), 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6", 
    install_requires=[
        'scapy', 
        'psutil',
        'speedtest-cli',
        'ping3',
    ],
    entry_points={ 
        "console_scripts": [
            "NetDiagnose = NetDiagnose.main:main", 
        ],
    },
)
