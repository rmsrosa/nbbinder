# Requirements

The NBBinder package uses the following standard libraries

- [re](https:/docs.python.org/3/library/re.html)
- [os](https:/docs.python.org/3/library/os.html)
- [itertools](https:/docs.python.org/3/library/itertools.html)
- [sys](https:/docs.python.org/3/library/sys.html)
- [logging](https:/docs.python.org/3/library/logging.html)

and the following nonstandard libraries:

- [nbformat](https://pypi.org/project/nbformat/),
- [nbconvert](https://pypi.org/project/nbconvert/)
- [pyyaml](https://pypi.org/project/PyYAML/).

The `nbformat` library is used to interact with the jupyter notebooks, the `nbconvert` library is used to export the notebooks to other formats (e.g. slides), and the `yaml` package is used, of course, to read the `*.yml` configuration files.

Exclusively for packaging for [PyPi](https://pypi.org), the following package is also used:

- [setuptools](https://pypi.org/project/setuptools/)