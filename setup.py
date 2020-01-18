from setuptools import setup, find_packages

setup(
    name='cogbooks',
    version='0.1',
    author='Petar Griggs',
    author_email='marrs2k@gmail.com',
    description='Use jupytext to convert instructor markdown files to student notebooks',
    url='https://github.com/CogWorksBWSI/Cogbooks',
    packages=find_packages(exclude=['tests', 'tests.*']),
    entry_points={'console_scripts': ['cogbooks = cogbooks:main']},
    python_requires=">=3.6",
    tests_require=['pytest', 'hypothesis'],
    install_requires=['jupytext'],
)
