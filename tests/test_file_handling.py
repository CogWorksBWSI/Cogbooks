from pathlib import Path
import os

tests_dir = Path(Path(__file__).resolve().parent)
jupy_dir = Path(tests_dir.parent)


def test_default_dir():
    os.system(
        f"cd {tests_dir / 'test_files'}\npython {jupy_dir / 'filter_notebooks.py'} ./"
    )
    tmpdir = Path(str(tests_dir / "test_files") + "_STUDENT")

    assert tmpdir.exists() and tmpdir.is_dir()
    for file in tmpdir.iterdir():
        assert (tests_dir / ("test_files/" + str(file.stem)[:-8] + ".md")).exists()

    os.system(f"rm -rf {tmpdir}")


def test_option_dir():
    tmpdir = tests_dir / "temp_dir"
    os.system(
        f"python {jupy_dir / 'filter_notebooks.py'} {tests_dir / 'test_files'} --dir {tmpdir}"
    )

    assert tmpdir.exists() and tmpdir.is_dir()
    for file in tmpdir.iterdir():
        assert (tests_dir / ("test_files/" + str(file.stem)[:-8] + ".md")).exists()

    os.system(f"rm -rf {tmpdir}")


def test_force():
    dir = tests_dir / "test_files"
    with open(dir / "test_STUDENT.ipynb", mode="r") as f:
        text = f.read()
    os.system(
        f"python {jupy_dir / 'filter_notebooks.py'} {tests_dir / 'test_files'} --dir {dir} --force"
    )
    with open(dir / "test_STUDENT.ipynb", mode="w+") as f:
        assert text != f.read()
        f.write(text)
