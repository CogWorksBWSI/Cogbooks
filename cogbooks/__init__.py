import argparse
import re
import os
from pathlib import Path


def strip_text(text: str) -> str:
    """
    Filters text between delimiters from markdown file

    Parameters
    ----------
    text : str
        Text of markdown file to filter

    Returns
    -------
    str
        Filtered markdown text
    """
    # First remove text from Python cells (with `# <COGINST>` delimiters)
    # and replace with a STUDENT CODE HERE comment
    stu_notebook = re.sub(
        r"# <COGINST>(.*?)</COGINST>", "# STUDENT CODE HERE", text, flags=re.S
    )

    # Remove text from markdown cells (with `<COGINST>` delimiters)
    # and replace with italicized `SOLUTION HERE`
    stu_notebook = re.sub(
        r"<COGINST>(.*?)</COGINST>", "*SOLUTION HERE*", stu_notebook, flags=re.S
    )

    # Remove instructor-only notes from markdown cells (with `<COGNOTE>` delimiters)
    stu_notebook = re.sub(r"<COGNOTE>(.*?)</COGNOTE>", "", stu_notebook, flags=re.S)

    # Remove single lines from code (with `<COGLINE>` addendum), preserving whitespace
    # and replace with a STUDENT CODE HERE comment
    return re.sub(r"\S(?<!\s)(.*?)<COGLINE>", "# STUDENT CODE HERE", stu_notebook)


def make_student_files(path: Path, outdir: Path, force: bool) -> bool:
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

    Returns
    -------
    Returns False if no file was written
    """

    if path.is_file() and path.suffix == ".md" and path.stem != "README":
        with open(path, mode="r") as f:
            stu_notebook = strip_text(f.read())

        file_path = outdir / (path.name[:-3] + "_STUDENT.md")

        if not force and (file_path.parent / (file_path.stem + ".ipynb")).exists():
            print(file_path.stem + ".ipynb" + " exists.. skipping file")
            return False

        with open(file_path, "w") as f:
            f.write(stu_notebook)

        # Convert to ipynb
        os.system(f'jupytext "{file_path.absolute()}" --to notebook')
        # Remove student markdown file
        os.remove(file_path)
        return True

    elif path.is_file():
        return False

    if not path.is_dir():
        print(f"{path.resolve().absolute()} does not exist")
        return False

    written = False
    for p in path.iterdir():
        if p.stem[0] != ".":
            written |= make_student_files(p, outdir, force)
    return written


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dir", "-d", help="specify output directory for student notebook files"
    )
    parser.add_argument(
        "--force",
        "-f",
        help="overwrites existing student notebooks",
        action="store_true",
    )
    parser.add_argument("files", nargs="*")

    args = parser.parse_args()

    written = False
    for p in args.files:
        p = Path(p)
        if args.dir is not None:
            out = Path(args.dir)

            if not out.exists():
                out.mkdir()
        elif p.is_file():
            out = p.parent
        else:
            out = p.resolve()

        written |= make_student_files(p, out, args.force)

    if not written:
        print(
            f"No files were written. The provided file-paths were: {' '.join(args.files)}"
        )


if __name__ == "__main__":
    main()
