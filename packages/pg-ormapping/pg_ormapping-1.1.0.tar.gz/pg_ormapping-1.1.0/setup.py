from setuptools import setup
from pg_ormapping import VERSION

DIST_NAME = "pg_ormapping"
__author__ = "baozilaji@gmail.com"

setup(
    name=DIST_NAME,
    version=VERSION,
    description="python game: ormapping",
    packages=[DIST_NAME],
    author=__author__,
    python_requires='>=3.9',
    install_requires=[
        'pg-redis',
        'pg-mongodb'
    ],
)
