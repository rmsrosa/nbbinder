# Requirements

## Main module nbbinder

The `nbbinder` module uses the standard libraries

- [re](https:/docs.python.org/3/library/re.html)
- [os](https:/docs.python.org/3/library/os.html)
- [itertools](https:/docs.python.org/3/library/itertools.html)
- [sys](https:/docs.python.org/3/library/sys.html)
- [logging](https:/docs.python.org/3/library/logging.html)
- [typing](https:/docs.python.org/3/library/typing.html)

and the nonstandard libraries

- [nbformat](https://pypi.org/project/nbformat/),
- [nbconvert](https://pypi.org/project/nbconvert/)
- [pyyaml](https://pypi.org/project/PyYAML/).

The `nbformat` library is used to interact with the jupyter notebooks, the `nbconvert` library is used to export the notebooks to other formats (e.g. slides, markdown, pdf), and the `yaml` package is used, of course, to read the `*.yml` configuration files.

## Test module

For testing `nbbinder`, the standard module

- [shutil](https:/docs.python.org/3/library/shutil.html)

and the nonstandard module

- [faker](https://pypi.org/project/faker/)

are also used.

## Packaging

Exclusively for packaging `nbbinder` for [PyPI](https://pypi.org) and [TestPyPI](https://test.pypi.org/), the following nonstandard package is used:

- [setuptools](https://pypi.org/project/setuptools/)
