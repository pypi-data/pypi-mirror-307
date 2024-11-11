# EducRating

Python package for rating systems usable in educational environments.

This package can be used to determine the proficiency of users and difficulty of items in an educational setting.
Currently there are three rating algorithms shipped:

- Elo Rating System (Elo)
  - with K-factor
  - with uncertainty function
- Multivariate Elo (M-Elo)
- Multivariate Glicko (MV-Glicko)

The package is available here: https://pypi.org/project/EducRating/

## Setup

To setup this repository, pull from the main branch.
The distribution files can then be build with `py -m build`.

#### For authors only

A `.pypirc`-file in the following format is needed to update the package on PyPI:

```
[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = <Enter your password here>
```

The package can be upload using the `twine upload -r testpypi dist/*` command.
Afterwards you will be asked to enter your API-Token which has to pasted in with `Edit > Paste`.

## Documentation

The documentation is provided via docline and can be generated as `HTML` via `pdoc --html src`.
To view it, open the `index.html`-file with your browser.

## Testing

All algorithms have been tested with Pytest.
You can run the tests by yourself using the `coverage run -m --branch pytest`.
The results will be shown inside the console with `coverage report -m`.
