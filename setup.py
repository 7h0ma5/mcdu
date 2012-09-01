from setuptools import setup

from glob import glob
import sys

if sys.platform == "darwin":
    extra_options = dict(
        app=["bin/mcdu"],
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
    scripts=["bin/mcdu"],
    **extra_options
)
