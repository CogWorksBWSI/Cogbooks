import argparse
import re
import os
from pathlib import Path


def strip_text(text):
    stu_notebook = re.sub(r"# <COGINST>(.*?)</COGINST>", "pass", text)
    return re.sub(r"<COGINST>(.*?)</COGINST>", "*SOLUTION HERE*", stu_notebook)


def make_student_files(path, outdir, force):
    """
    Creates student Jupyter notebooks given Jupytext markdown files

    Parameters
    ----------
    path : pathlib.Path
        Path to an existing markdown file or directory containing markdown files

    outdir : pathlib.Path
        Path to directory which will contain student notebooks

    force : bool
        Signals that existing student notebooks should be overwritten
    """

    if path.is_file() and path.suffix == ".md":
        with open(path, mode="r") as f:
            stu_notebook = strip_text(repr(f.read()))

        file_path = outdir / (str(path.stem) + "_STUDENT.md")
        if force:
            with open(file_path, mode="w") as f:
                f.write(eval(stu_notebook))
        else:
            if file_path.with_suffix(".ipynb").is_file():
                print(f"{file_path.with_suffix('.ipynb')} already exists")
            else:
                try:
                    with open(file_path, mode="x") as f:
                        f.write(eval(stu_notebook))
                except:
                    print(f"{file_path} already exists")

        os.system(f"jupytext {file_path} --to notebook >/dev/null 2>&1")
        os.system(f"rm {file_path}")

    elif path.is_dir():
        for p in path.iterdir():
            if p.stem[0] != ".":
                make_student_files(p, outdir, force)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dir", "-d", help="specify out directory for student notebook files"
    )
    parser.add_argument(
        "--force",
        "-f",
        help="overwrites existing student notebooks",
        action="store_true"
    )
    parser.add_argument("files", nargs="*")

    args = parser.parse_args()

    if args.dir is not None:
        out = Path(args.dir)
    else:
        out = Path(str(Path(".").absolute()) + "_STUDENT")
    if not out.exists():
        out.mkdir()

    for p in args.files:
        make_student_files(Path(p), out, args.force)
