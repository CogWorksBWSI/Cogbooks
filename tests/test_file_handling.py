import shutil
from hypothesis import given, settings
import hypothesis.strategies as st
import os
from pathlib import Path
import pytest


@pytest.mark.usefixtures("cleandir")
def test_dir_ipynb_doesnt_exist():
    dest = Path(".") / "test_files" / "test_STUDENT.ipynb"
    os.remove(dest)
    assert not dest.exists()
    os.system(f"cogbooks test_files")
    assert dest.exists()


@pytest.mark.usefixtures("cleandir")
def test_file_ipynb_doesnt_exist():
    dest = Path(".") / "test_files" / "test_STUDENT.ipynb"
    os.remove(dest)
    assert not dest.exists()
    os.system(f"cogbooks test_files/test.md")
    assert dest.exists()


@pytest.mark.usefixtures("cleandir")
@settings(deadline=None, max_examples=10)
@given(num_files=st.sampled_from(range(4)), already_exists=st.lists(st.sampled_from(range(4)), unique=True))
def test_multiple_files_in_dir_where_some_exist(num_files: int, already_exists: list):
    Path("./dummy").mkdir(exist_ok=True)
    for i in range(num_files):
        shutil.copy('test_files/test.md', f'dummy/test{i}.md')

    for i in already_exists:
        Path(f'dummy/test{i}_STUDENT.ipynb').touch()

    os.system(f"cogbooks dummy")
    assert all([Path(f'dummy/test{i}_STUDENT.ipynb').exists() for i in range(num_files)])
    shutil.rmtree(Path("./dummy"))


@pytest.mark.usefixtures("cleandir")
@settings(deadline=None, max_examples=10)
@given(num_files=st.sampled_from(range(4)), already_exists=st.lists(st.sampled_from(range(4)), unique=True))
def test_multiple_files_where_some_exist(num_files: int, already_exists: list):
    Path("./dummy").mkdir(exist_ok=True)
    for i in range(num_files):
        shutil.copy('test_files/test.md', f'dummy/test{i}.md')

    for i in already_exists:
        Path(f'dummy/test{i}_STUDENT.ipynb').touch()

    list_of_names = ' '.join([f'dummy/test{i}.md' for i in set(list(range(num_files)) + already_exists)])
    os.system(f"cogbooks {list_of_names}")
    assert all([Path(f'dummy/test{i}_STUDENT.ipynb').exists() for i in range(num_files)])
    shutil.rmtree(Path("./dummy"))
