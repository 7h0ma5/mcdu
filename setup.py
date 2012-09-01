from setuptools import setup

from glob import glob
import sys

if sys.platform == "darwin":
    extra_options = dict(
        app=["mcdu/main.py"],
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
    license="GNU GPL v3",
    version="1.0",
    tests_require='nose',
    test_suite='nose.collector',
    packages=["mcdu"],
    scripts=["mcdu/main.py"],
    data_files = [
        ("mcdu", glob("config/*")),
        ("mcdu", glob("res/*")),
    ],
    **extra_options
)
