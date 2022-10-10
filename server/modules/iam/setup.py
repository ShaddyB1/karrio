from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="karrio.server.iam",
    version="2022.10",
    description="Multi-carrier shipping API iam module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karrioapi/karrio",
    author="karrio",
    author_email="hello@karrio.io",
    license="GPLv3",
    packages=find_namespace_packages(exclude=["tests.*", "tests"]),
    install_requires=[
        "karrio.server.core",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    zip_safe=False,
    include_package_data=True,
)
