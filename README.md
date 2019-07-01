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