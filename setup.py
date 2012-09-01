from setuptools import setup
from glob import glob
import sys

if sys.platform == "darwin":
    extra_options = dict(
        setup_requires=["py2app"],
        options=dict(
            py2app=dict(
                arch="i386",
                argv_emulation=True
            )
        )
    )
else:
    extra_options = dict()

setup(
    name="MCDU",
    license="GPL",
    version="1.0",
    app=["main.py"],
    data_files = [
        ("config", glob("config/*")),
        ("res", glob("res/*")),
    ],
    **extra_options
)
