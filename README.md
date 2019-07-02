# Cogbooks
Provides a tool for CogWorks instructors and TAs to filter instructor-only material out of Jupytext markdown files to create student Jupyter notebooks.

# Installation Instructions
First, install Jupytext by running
```shell
conda install -c conda-forge jupytext
```

Once you have installed Jupytext, clone this repository, navigate to it, and run

```shell
python setup.py develop
```

# Usage
After installing Cogbooks, to convert a markdown file to a student notebook, run
```shell
cogbooks activitiy.md
```

Cogbooks will create the file `activity_STUDENT.ipynb` in the same directory as `activity.md`. A directory (which may or may not exist) to write student notebooks to can be specified with `--dir` or `-d`:
```shell
cogbooks activitiy.md --dir out_directory
```

Directories or multiple markdown files can be passed to Cogbooks:
```shell
cogbooks day1_directory/ activity1.md activity2.md
```

By default, existing notebooks will not be overwritten. Specifying `--force` or `-f` will have Cogbooks rewrite existing student notebooks.


# Delimiting
Any instructor-only markdown file should be properly delimited. In Python code, use:
```python
set-up code here
# <COGINST>
instructor-only code here
# </COGINST>
```
Running Cogbooks will then yield:
```python
set-up code here
pass
```

In markdown, use:
```markdown
question here
<COGINST>
instructor-only answer here
</COGINST>
```

yielding,
```markdown
question here
*SOLUTION HERE*
```

Lastly, to leave an instructor-only note in a markdown cell, use:
```markdown
random text here
<COGNOTE>
instructor-only note here
</COGNOTE>
more random text here
```

which results in,
```markdown
random text here
more random text here
```