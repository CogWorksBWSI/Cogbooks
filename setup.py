import versioneer
from setuptools import setup, find_packages

DESCRIPTION = "Convert instructor jupytext-markdown to student notebooks, removing all solutions"
LONG_DESCRIPTION = """
The idea of using jupytext for CogWorks is this: Editing notebooks is painful. Doing version control on notebooks is 
painful. Giving students notebooks is great. So, as instructors, we will develop all of our material in markdown files 
and then we will use `cogbooks` to convert our markdown files to jupyter notebooks.

What is great about this is, `cogbooks` introduces special markdown delimiters that permit instructors to include 
solutions and instructors-eyes-only comments in a markdown file, so that the file contains the full solutions. 
`cogbooks` will then excise these sections when it converts the instructor-markdown files to student-notebooks. 
"""

setup(
    name='cogbooks',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Petar Griggs',
    author_email='marrs2k@gmail.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url='https://github.com/CogWorksBWSI/Cogbooks',
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=['tests', 'tests.*']),
    entry_points={'console_scripts': ['cogbooks = cogbooks:main']},
    python_requires=">=3.6",
    tests_require=['pytest', 'hypothesis'],
    install_requires=['jupytext >= 1.2.0'],
)
