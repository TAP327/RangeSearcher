from setuptools import setup

setup(
    name='RangeSubsidiary',
    version='0.1.0',
    packages=['RangeSubsidiary'],
    install_requires=[
        "flask",
        "pandas",
        "pathlib",
        "regex"
    ],
    entry_points={
        'console_scripts': [
            'rs=RangeSubsidiary.main:main',
        ],
    },
)
