import setuptools
with open("README.md", "r", encoding = 'utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="guandan",
    version="0.0.1",
    author="afan",
    author_email="fcncassandra@gmail.com",
    description="guandan tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AFAN-LIFE/guandan",
    packages=setuptools.find_packages(),
    license='Apache License',
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)