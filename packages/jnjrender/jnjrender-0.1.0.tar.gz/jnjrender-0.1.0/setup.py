# setup.py

from setuptools import setup, find_packages

setup(
    name="jnjrender",
    version="0.1.0",
    packages=find_packages(),
    description="A utility to render Jinja2 templates in rendered text",
    author="Andrea Michelotti",
    install_requires=[
        "jinja2",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "jnjrender=jnjrender.cli:main",
        ],
    },
)
