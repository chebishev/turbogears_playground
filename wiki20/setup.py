from setuptools import setup

install_requires=[
    "TurboGears2 >= 2.3.9",
    "Babel",
    "Beaker",
    "Kajiki",
    "zope.sqlalchemy >= 0.4",
    "sqlalchemy",
    "alembic",
    "repoze.who",
    "tw2.forms",
    "tgext.admin >= 0.6.1",
    "WebHelpers2",
    "docutils"
]

if __name__ == "__main__":
    setup()