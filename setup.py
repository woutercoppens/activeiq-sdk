import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="activeiq-sdk",
    version="0.0.1",
    author="Wouter Coppens",
    author_email="wouter.coppens@gmail.com",
    description="This package allows to consume the ActiveIQ API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/woutercoppens/activeiq-sdk",
    packages=setuptools.find_namespace_packages(include=['activeiq.*']),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache 2.0 License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests-oauthlib>=1.2.0',
        'future>=0.18.2'
    ],
    python_requires='>=3.5',
)
