from setuptools import setup, find_packages
from docketpy import __version__

setup(
    name="docketpy",
    version=__version__,
    packages=find_packages(include=("docketpy", "docketpy.*")),
    description='Docket Python library',
    author='VST',
    license='MIT',
    install_requires=[
        "dill",
        "redis",
        "numpy",
        "google-cloud-storage",
        "google-cloud-bigquery",
        "SQLAlchemy",
        "sqlalchemy-utils",
        "psycopg2-binary",
        ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
