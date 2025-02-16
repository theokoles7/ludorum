"""Ludorum setup utility."""

from setuptools import find_packages, setup

setup(
    name =              "ludorum",
    version =           "0.0.1",
    author =            (
                            "Gabriel C. Trahan, "
                            "Christopher J. Langley"
                        ),
    author_email =      (
                            "gabriel.trahan1@louisiana.edu, "
                            "christopher.langely1@louisiana.edu"
                        ),
    description =       (
                            "Suite of environments, models, & methods in pursuit of achieving "
                            "organic reasoning & logic by means of deep reinforcement learning."
                        ),
    license =           "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007",
    license_files =     ("LICENSE"),
    url =               "https://github.com/theokoles7/ludorum",
    packages =          find_packages(),
    python_requires =   ">=3.10",
    install_requires =  [
                            "matplotlib",
                            "numpy",
                            "termcolor",
                            "torch",
                            "tqdm"
                        ]
)