from os.path import sep, join
from os import environ

__all__ = ("init_env","DD_ROOT", "DD_SHOWS_ROOT")

DD_ROOT = "DD_ROOT"
DD_SHOWS_ROOT = "DD_SHOWS_ROOT"
FAUXIT_HOME = "FAUXIT_HOME"
def init_env():
    home = environ.get(FAUXIT_HOME, environ.get("HOME"))
    environ[DD_ROOT] =  join(sep, home,"dd")
    environ[DD_SHOWS_ROOT] =join(sep, home, "dd", "SHOWS")
