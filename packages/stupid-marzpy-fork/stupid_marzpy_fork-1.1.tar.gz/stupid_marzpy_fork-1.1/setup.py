from setuptools import setup, find_packages

with open("README.md", "r") as file:
    readme = file.read()

setup(
    name="stupid_marzpy_fork",
    version="1.1",
    author="tol144",
    author_email="toltol1992toltol@gmail.com",
    description="a simple application with python to manage Marzban panel",
    long_description="text/markdown",
    url="https://github.com/tol144/stupid_marzpy_fork",
    keywords=["marzpy", "Marzban", "Gozargah", "Marzban python", "Marzban API"],
    packages=find_packages(),
    install_requires=["aiohttp"],
    classifiers=["Programming Language :: Python :: 3"],
)
