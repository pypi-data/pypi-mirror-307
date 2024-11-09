"""Setup the pypi package."""

import setuptools  # type: ignore[import]

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setuptools.setup(
    name="pylamarzocco",
    version="1.2.3",
    description="A Python implementation of the new La Marzocco API",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/zweckj/pylamarzocco",
    author="Josef Zweck",
    author_email="24647999+zweckj@users.noreply.github.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        "httpx>=0.16.1",
        "websockets>=11.0.2",
        "bleak>=0.20.2",
    ],
    package_data={
        "pylamarzocco": ["py.typed"],
    },
)
