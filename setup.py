from setuptools import setup, find_packages

setup(
    name="hudson",
    entry_points={
        "console_scripts": [
            "HudsonBE = hudson.app:main"
        ]
    },
)