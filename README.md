# Cogbooks
Provides a tool for CogWorks instructors and TAs to filter instructor-only material out of [Jupytext markdown](https://jupytext.readthedocs.io/en/latest/introduction.html) files to create student Jupyter notebooks.

The idea of using jupytext for CogWorks is this: Editing notebooks is painful. Doing version control on notebooks is painful. Giving students notebooks is great. So, as instructors, we will develop all of our material in markdown files and then we will use `cogbooks` to convert our markdown files to jupyter notebooks.

What is great about this is, `cogbooks` introduces special markdown delimiters that permit instructors to include solutions and instructors-eyes-only comments in a markdown file, so that the file contains the full solutions. `cogbooks` will then excise these sections when it converts the instructor-markdown files to student-notebooks. 

For example, a markdown-file containing:

````
Make a list of the first 100 perfect squares
```python
# <COGINST>
solution = [i**2 for i in range(100)]
# </COGINST>
```
````
Running `cogbooks` will then yield a jupyter notebook containing:
```
Make a list of the first 100 perfect squares
```
```python
# STUDENT CODE HERE
```


# Installation Instructions
Clone this repository, navigate to it, and run

```shell
python setup.py install
```

# Usage
After installing Cogbooks, to convert a markdown file to a student notebook, run
```shell
cogbooks activitiy.md
```

Cogbooks will create the file `activity_STUDENT.ipynb` in the same directory as `activity.md`. Or, a directory to write student notebooks to can be specified with `--dir` or `-d`:
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
