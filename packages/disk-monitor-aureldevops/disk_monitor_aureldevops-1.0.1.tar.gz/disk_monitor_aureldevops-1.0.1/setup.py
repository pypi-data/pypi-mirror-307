from setuptools import setup, find_packages
import disk_monitor

setup(
    name="disk_monitor_aureldevops",
    version=disk_monitor.__version__,
    author=disk_monitor.__author__,
    description="Module de surveillance d'espace disque",
    long_description="Module python pour surveiller l'espace disque en fonction d'un chemin et d'un seuil",
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11'
)