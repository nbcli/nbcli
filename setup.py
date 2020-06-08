import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = {'__builtins__': None}

with open("netbox-client/__version__.py", "r") as fh:
    exec(fh.read(), version)

del version["__builtins__"]

setuptools.setup(
    name="netbox-client",
    version=version["__version__"],
    author="Eric Geldmacher",
    author_email="egeldmacher@wustl.edu",
    description="CLI and shell for netbox using pynetbox module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/egeldmacher/netbox-client",
    license="GPLv3",
    packages=setuptools.find_packages(),
    install_requires=["pynetbox"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "nbcli=netbox_client.cli:main",
            "nbshell=netbox_client.shell:main",
        ],
    },
)
