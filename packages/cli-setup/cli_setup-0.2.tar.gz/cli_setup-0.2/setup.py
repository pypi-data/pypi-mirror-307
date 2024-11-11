from setuptools import setup, find_packages

setup(
    name="cli_setup",
    version='0.2',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        "console_scripts": [
            "cli-cmd = cli_package:hello"
        ]
    }
)
