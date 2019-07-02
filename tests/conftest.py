import os
import shutil
import tempfile
from pathlib import Path

import pytest

data_dir = Path(Path(__file__).resolve().parent) / 'test_files'


@pytest.fixture()
def cleandir() -> str:
    """ This fixture will use the stdlib `tempfile` module to
    move the current working directory to a tmp-dir for the
    duration of the test.
    Afterwards, the session returns to its previous working
    directory, and the temporary directory and its contents
    are removed.

    Yields
    ------
    str
        The name of the temporary directory."""

    with tempfile.TemporaryDirectory() as tmpdirname:
        old_dir = os.getcwd()
        os.chdir(tmpdirname)
        os.mkdir('test_files')
        dest = Path.cwd() / 'test_files'
        shutil.copy(data_dir / 'test.md', dest)
        shutil.copy(data_dir / 'test_STUDENT.ipynb', dest)
        yield tmpdirname
        os.chdir(old_dir)
