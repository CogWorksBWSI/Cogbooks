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
    assert len(list((Path(".") / "test_files").glob("*.ipynb"))) == 1


@pytest.mark.usefixtures("cleandir")
def test_file_ipynb_doesnt_exist():
    dest = Path(".") / "test_files" / "test_STUDENT.ipynb"
    os.remove(dest)
    assert not dest.exists()
    os.system(f"cogbooks test_files/test.md")
    assert dest.exists()


@pytest.mark.usefixtures("cleandir")
def test_no_extra_md_files_are_written_or_removed():
    root = Path("./test_files").resolve()
    all_files = {path: os.path.getsize(path) for path in root.glob("*.md")}
    os.system(f"cogbooks --force test_files")
    assert all_files == {path: os.path.getsize(path) for path in root.glob("*.md")}


@pytest.mark.usefixtures("cleandir")
@settings(deadline=None, max_examples=20)
@given(
    num_files=st.sampled_from(range(4)),
    data=st.data(),
    force=st.booleans(),
    specify_files=st.booleans(),
)
def test_multiple_files_in_dir_where_some_exist(
    num_files: int, data: st.DataObject, force: bool, specify_files: bool
):
    # draw the ipynb files that will already exist
    if num_files:
        already_exists = data.draw(
            st.lists(st.sampled_from(range(num_files)), unique=True)
        )
    else:
        already_exists = []

    # prep the directory for the md and ipynb files
    dummy_dir = Path("./dummy")

    if dummy_dir.exists():
        shutil.rmtree(dummy_dir)

    dummy_dir.mkdir(exist_ok=False)

    # create the md files
    for i in range(num_files):
        shutil.copy("test_files/test.md", f"dummy/test{i}.md")

    # ensure the ipynb files are not already present
    assert all(
        [not (dummy_dir / f"test{i}_STUDENT.ipynb").exists() for i in range(num_files)]
    ), "ipynb files are already present prior to running the cogbooks"

    # create pre-existing ipynb files as empty files
    for i in already_exists:
        (dummy_dir / f"test{i}_STUDENT.ipynb").touch()
        assert (
            os.path.getsize(dummy_dir / f"test{i}_STUDENT.ipynb") == 0
        ), "pre-existing files should be empty"

    # invoke cogbooks with either the dir as an argument, or sequence of md files
    if specify_files:
        list_of_names = " ".join(
            [f"dummy/test{i}.md" for i in set(list(range(num_files)) + already_exists)]
        )
        cmd = f"cogbooks {list_of_names}"
    else:
        cmd = f"cogbooks dummy"

    os.system(cmd + (" --force" if force else ""))

    # ensure all ipynb files exist
    assert all(
        [(dummy_dir / f"test{i}_STUDENT.ipynb").exists() for i in range(num_files)]
    )

    # ensure pre-existing ipynb files are overwritten only when --force was specified
    # otherwise they should be empty
    for i in already_exists:
        file = f"./dummy/test{i}_STUDENT.ipynb"
        if not force:
            assert (
                os.path.getsize(file) == 0
            ), f"a pre-existing file was overwritten: {file}"
        else:
            assert (
                os.path.getsize(file) > 0
            ), f"--force failed to overwrite pre-existing notebook: {file}"

    # ensure that the ipynb files that created via cogbooks are not empty
    for i in range(num_files):
        if i in already_exists:
            continue
        assert (
            os.path.getsize(f"./dummy/test{i}_STUDENT.ipynb") > 0
        ), "the converted notebook is empty"
