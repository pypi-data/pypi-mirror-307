"""
invoke file for the Ciqar project.

(This is similar to a 'Makefile' - see https://www.pyinvoke.org/)
"""

from datetime import datetime
import fileinput
from pathlib import Path

from invoke import Context, task


@task
def depupgrade(ctx: Context) -> None:
    """
    Upgrade all dependencies and update requirements-dev.txt (by running `pip-compile --upgrade`).
    """
    ctx.run("pip-compile --upgrade --extra devtools --resolver=backtracking -o requirements-dev.txt pyproject.toml > /dev/null")


@task
def depsync(ctx: Context) -> None:
    """
    Synchronize the current environment with the requirements-dev.txt (by running `pip-sync`).
    """
    ctx.run("pip-sync requirements-dev.txt")

@task
def bump(ctx: Context, version_string: str) -> None:
    """
    Set all version information to the specified version string (and today's date).
    """

    release_date = datetime.today().strftime("%Y-%m-%d")

    # Set version header in CHANGELOG file
    changelog_file = Path("CHANGELOG.md")
    for line in fileinput.input(files=changelog_file, inplace=True):
        print(line.rstrip())
        if line.startswith("## [Unreleased]"):
            print(f"\n## [{version_string}] - {release_date}")

    # Set application version string
    version_src_file = Path("src/ciqar/__init__.py")
    for line in fileinput.input(files=version_src_file, inplace=True):
        if line.startswith("__version__ = "):
            line = f"__version__ = \"{version_string}\""
        print(line.rstrip())

@task
def test(ctx: Context) -> None:
    """
    Run all unit tests and create a HTML code coverage report.
    """
    ctx.run("PYTHONPATH=src py.test")

@task
def mypy(ctx: Context) -> None:
    """
    Analyze all sources using MyPy.
    """
    ctx.run("mypy --config-file mypy.ini --junit-xml junit-mypy.xml src test | tee mypy.log")


@task
def pyright(ctx: Context) -> None:
    """
    Analyze all sources using Pyright.
    """
    ctx.run("pyright --outputjson src test > pyright.json")

@task
def pylint(ctx: Context) -> None:
    """
    Analyze all sources using Pylint.
    """
    ctx.run("pylint --rcfile=pylint.rc --recursive=y src test")

@task
def ruff(ctx: Context) -> None:
    """
    Analyze all sources using ruff.
    """
    ctx.run("python -m ruff check src/ test/ --output-format json > ruff.json")

@task
def build(ctx: Context) -> None:
    """
    Build PyPI package.
    """
    ctx.run("flit build")

@task
def black(ctx: Context) -> None:
    """
    Check if any source file would be reformatted by black.
    """
    ctx.run("black src test --check --verbose 2>black.log || true")
    ctx.run("black-junit < black.log > junit-black.xml")

@task
def format(ctx: Context) -> None:
    """
    Run black on the whole code base.
    """
    ctx.run("black src test")
