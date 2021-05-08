from setuptools import find_packages, setup

setup(
    name="blockchain",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    entry_points="""
        [console_scripts]
        blockchain=blockchain.cli:main
    """,
)
