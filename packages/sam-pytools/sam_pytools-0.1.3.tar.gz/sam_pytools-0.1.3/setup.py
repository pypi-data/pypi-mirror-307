from setuptools import find_namespace_packages, setup

setup(
    name='sam-djtools',
    long_description_content_type="text/markdown",
    url="https://github.com/humblesami/sam-djtools.git",
    python_requires=">=3",
    setup_requires=['setuptools_scm'],
    data_files=[],
    packages=find_namespace_packages(include=["sam_pytools"],),
)
