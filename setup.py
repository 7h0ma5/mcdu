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
        ),
        data_files = [
            ("config", glob("config/*")),
            ("res", glob("res/*"))
        ],
    )
elif sys.platform == "win32":
    import py2exe
    extra_options = dict(
        console=[{"script": "mcdu/main.py", "dest_base": "mcdu"}],
        options=dict(
            py2exe={
                "includes": ["pyuipc", "pyglet"],
                "bundle_files": 1,
                "compressed": True,
                "dll_excludes": ["w9xpopen.exe"],
            }
        ),
        data_files = [
            ("config", glob("config/*")),
	    ("res", glob("res/*")),
	],
        zipfile=None,
    )
else:
    extra_options = dict(
        data_files = [
            ("share/mcdu/config", glob("config/*")),
            ("share/mcdu/res", glob("res/*"))
        ],
    )

setup(
    name="MCDU",
    license="GNU GPL v3",
    author="Thomas Gatzweiler",
    author_email="mail@thomasgatzweiler.com",
    url="https://github.com/7h0ma5/mcdu/",
    version="1.0",
    packages=["mcdu"],
    scripts=["bin/mcdu"],
    **extra_options
)
