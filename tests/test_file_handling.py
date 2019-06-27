from pathlib import Path
import os


def test_default_dir():
    os.system(f"cd {Path('./tests/test_files')}\npython {Path('../../filter_notebooks.py')} ./")
    tmpdir = Path(str(Path("./tests/test_files").absolute()) + "_STUDENT")

    assert tmpdir.exists() and tmpdir.is_dir()
    for file in tmpdir.iterdir():
        assert Path("./tests/test_files/" + str(file.stem)[:-8] + ".md").exists()

    os.system(f"rm -rf {tmpdir}")


def test_option_dir():
    tmpdir = Path(".").resolve() / "tests/temp_dir"
    os.system(
        f"python {Path('./filter_notebooks.py').resolve()} tests/test_files --dir {tmpdir}"
    )

    assert tmpdir.exists() and tmpdir.is_dir()
    for file in tmpdir.iterdir():
        assert Path("./tests/test_files/" + str(file.stem)[:-8] + ".md").exists()

    os.system(f"rm -rf {tmpdir}")


def test_force():
    dir = Path("./tests/test_files")
    os.system(
        f"python {Path('../filter_notebooks.py').resolve()} test_files --dir {dir} --force"
    )
    with open(dir / "test_STUDENT.ipynb", mode="a+") as f:
        assert f.read()[-4:] != "TEST"
        f.write("TEST")
