from setuptools import setup
from setuptools import find_packages

setup(
    name="pseu",
    description="Pseudorandom utils for the CLI.",
    version="1.0.0",
    url="https://github.com/Kevinpgalligan/pseu",
    author="Kevin Galligan",
    author_email="galligankevinp@gmail.com",
    packages=find_packages("src"),
    package_dir={'': 'src'},
    install_requires=[]
)
