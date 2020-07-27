import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = dict()

with open("nbcli/__version__.py", "r") as fh:
    exec(fh.read(), dict(), version)

setuptools.setup(
    name="nbcli",
    version=version["__version__"],
    author="Eric Geldmacher",
    author_email="egeldmacher@wustl.edu",
    description="CLI for netbox using pynetbox module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ericgeldmacher/nbcli",
    license="GPLv3",
    packages=setuptools.find_packages(),
    package_data={
        'nbcli': ['user_defaults/*.default']
    },
    install_requires=["pynetbox>=5.0.3", 'pyyaml'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "nbcli=nbcli.cli:main",
        ],
    },
)
