import argparse
import re
import os
from pathlib import Path


def make_stu_files(path, outdir):
    if path.suffix == ".ipynb":
        os.system(f"jupytext {path} --to markdown >/dev/null 2>&1")

    with open(path.with_suffix(".md"), mode="r") as f:
        stu_notebook = re.sub(r"(# |)<COGINST>(.*?)</COGINST>", "pass", repr(f.read()))

    file_path = outdir / (str(path.stem) + "_STUDENT.md")
    with open(file_path, mode="w") as f:
        f.write(eval(stu_notebook))

    os.system(f"jupytext {str(file_path)} --to notebook >/dev/null 2>&1")
    os.system(f"rm {str(file_path)}")


def convert_args(path):
    if path.is_file() and (
        path.suffix == ".ipynb"
        or (path.suffix == ".md" and os.system(f"jupytext {path} --paired-paths"))
    ):
        make_stu_files(path, outdir)

    elif path.is_dir():
        for p in path.iterdir():
            if str(p.stem)[0] != ".":
                convert_args(p)

    else:
        print(f"{path} is not a valid directory or markdown file")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dir", "-d", help="specify directory for student notebook files"
    )
    parser.add_argument("files", nargs="*")

    args = parser.parse_args()

    if args.dir is not None:
        outdir = Path(args.dir)
    else:
        outdir = Path(str(Path(".").absolute()) + "_STUDENT")
    if not outdir.exists():
        outdir.mkdir()

    for p in args.files:
        convert_args(Path(p))
