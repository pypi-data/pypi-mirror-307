from setuptools import setup, find_packages

def parse_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name="GetADSILO",
    version="0.1",
    description="GetADSILO is a Python script that queries Active Directory to list users and computers associated with authentication silos.",
    author="WiseLife",
    author_email="",
    url="https://github.com/WiseLife42/GetADSILO",
    packages=find_packages(),
    install_requires=parse_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'getadsilo=getadsilo.getadsilo:main',
        ],
    },
)
