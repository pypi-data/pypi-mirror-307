import io

import setuptools

with io.open("README.md", encoding="utf-8") as f:
    readme = f.read()

setuptools.setup(
    name="yamcs-client-kerberos",
    version="1.3.0",
    description="Kerberos integration for Yamcs API client library",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/yamcs/python-yamcs-client/yamcs-client-kerberos",
    author="Space Applications Services",
    author_email="yamcs@spaceapplications.com",
    license="LGPL",
    packages=setuptools.find_namespace_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    platforms="Posix; MacOS X; Windows",
    install_requires=["requests-kerberos", "yamcs-client>=1.11.0"],
    include_package_data=True,
    zip_safe=False,
)
