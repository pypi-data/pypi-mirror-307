from setuptools import setup, find_packages
import shutil

shutil.rmtree("dist")

setup(
    name="kimopy",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[]
)