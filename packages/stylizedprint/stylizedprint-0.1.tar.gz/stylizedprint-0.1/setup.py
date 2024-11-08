from setuptools import setup, find_packages

setup(
    name="stylizedprint",
    version="0.1",
    description="A package for creating stylish console prints with ease",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Unai Zubeldia, Ruben Jordana, Peio Garcia",
    maintainer="Unai Zubeldia, Ruben Jordana, Peio Garcia",
    maintainer_email="unai.zubeldia@alumni.mondragon.edu, ruben.jordana@alumni.mondragon.edu, peio.garcia@alumni.mondragon.edu",
    url="https://github.com/unaizubeldia/stylizedprint",
    packages=find_packages(),
    install_requires=["colorama", "rich"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
