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
    # and replace with a pass statement
    stu_notebook = re.sub(r"# <COGINST>(.*?)</COGINST>", "pass", text)

    # Remove text from markdown cells (with `<COGINST>` delimiters)
    # and replace with italicized `SOLUTION HERE`
    return re.sub(r"<COGINST>(.*?)</COGINST>", "*SOLUTION HERE*", stu_notebook)


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

    if path.is_file() and path.suffix == ".md":
        with open(path, mode="r") as f:
            # Apply repr as to escape \n characters
            # as Regex requires singular line of text
            stu_notebook = strip_text(repr(f.read()))

        file_path = outdir / (path.name[:-3] + "_STUDENT.md")

        if not force and (file_path.parent / (file_path.stem + '.ipynb')).exists():
            print(file_path.stem + '.ipynb' + " exists.. skipping file")
            return False

        with open(file_path, 'w') as f:
            # Apply eval to convert raw string to string
            # and recover newline formatting for output file
            # (Jupytext doesn't properly convert markdown if not done)
            f.write(eval(stu_notebook))

        # Convert to ipynb, silencing outputs from Jupytext
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
    parser.add_argument("files", nargs="*", )

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
        print(f"No files were written. The provided file-paths were: {''.join(args.files)}")


if __name__ == "__main__":
    main()

