import os
from posixpath import abspath, expanduser
import shutil


joinpaths: callable = os.path.join

def mkdirs(
    name,
    mode: int = 511,
    exist_ok: bool = False
):
    os.makedirs(name=name, mode=mode, exist_ok=exist_ok)

def rmfile(
    path,
):
    os.remove(path=path)

def rmdirs(
    name,
):
    os.removedirs(name=name)

def rmtree(
    path,
):
    shutil.rmtree(path=path)

pathexists: callable = os.path.exists
_: callable = abspath, expanduser

current_working_dir: str = os.getcwd()
