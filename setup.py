import versioneer
from setuptools import setup, find_packages

setup(
    name='cogbooks',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Petar Griggs',
    author_email='marrs2k@gmail.com',
    description='Use jupytext to convert instructor markdown files to student notebooks',
    url='https://github.com/CogWorksBWSI/Cogbooks',
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=['tests', 'tests.*']),
    entry_points={'console_scripts': ['cogbooks = cogbooks:main']},
    python_requires=">=3.6",
    tests_require=['pytest', 'hypothesis'],
    install_requires=['jupytext'],
)
