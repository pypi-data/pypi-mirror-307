import os
from setuptools import setup
#
#
#
#
def get_install_requires():
    lib_folder = os.path.dirname(os.path.realpath(__file__))
    requirement_path = f"{lib_folder}/requirements.txt"

    install_requires = []

    if os.path.isfile(requirement_path):
        install_requires = open(requirement_path, "r", encoding="utf-8").read().splitlines()

    return install_requires
#
#
#
#
setup(
		name="PyWebScraping",
		version="1.01",
		author="oddshellnick",
		author_email="oddshellnick.programming@gmail.com",
		packages=["PyWebScraping", "PyWebScraping.webdrivers"],
		install_requires=get_install_requires()
)
