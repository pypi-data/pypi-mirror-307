from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="cli_setup",
    version='0.3',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        "console_scripts": [
            "cli-cmd = cli_package:hello"
        ]
    },
    long_description=description,
    long_description_content_type="text/markdown"
)
