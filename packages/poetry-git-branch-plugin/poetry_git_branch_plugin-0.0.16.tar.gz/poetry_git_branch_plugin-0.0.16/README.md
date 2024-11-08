Poetry Git Branch Plugin
==========================

<p align="center">
    <a href="https://dribia.github.io/driconfig">
        <picture style="display: block; margin-left: auto; margin-right: auto; width: 40%;">
            <source
                media="(prefers-color-scheme: dark)"
                srcset="https://dribia.github.io/driconfig/img/logo_dribia_blanc_cropped.png"
            >
            <source
                media="(prefers-color-scheme: light)"
                srcset="https://dribia.github.io/driconfig/img/logo_dribia_blau_cropped.png"
            >
            <img
                alt="driconfig"
                src="https://dribia.github.io/driconfig/img/logo_dribia_blau_cropped.png"
            >
        </picture>
    </a>
</p>

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CI/CD   | [![Tests](https://github.com/dribia/poetry-git-branch-plugin/actions/workflows/test.yml/badge.svg)](https://github.com/dribia/poetry-git-branch-plugin/actions/workflows/test.yml) [![Coverage Status](https://img.shields.io/codecov/c/github/dribia/poetry-git-branch-plugin)](https://codecov.io/gh/dribia/poetry-git-branch-plugin) [![Tests](https://github.com/dribia/poetry-git-branch-plugin/actions/workflows/lint.yml/badge.svg)](https://github.com/dribia/poetry-git-branch-plugin/actions/workflows/lint.yml) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) |
| Package | [![PyPI](https://img.shields.io/pypi/v/poetry-git-branch-plugin)](https://pypi.org/project/poetry-git-branch-plugin/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/poetry-git-branch-plugin?color=blue&logo=pypi&logoColor=gold) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/poetry-git-branch-plugin?logo=python&logoColor=gold) [![GitHub](https://img.shields.io/github/license/dribia/poetry-git-branch-plugin?color=blue)](LICENSE)                                                                                                                                                                                                                                                                                                         |
---

**Documentation**: <a href="https://dribia.github.io/poetry-git-branch-plugin" target="_blank">https://dribia.github.io/poetry-git-branch-plugin</a>

**Source Code**: <a href="https://github.com/dribia/poetry-git-branch-plugin" target="_blank">https://github.com/dribia/poetry-git-branch-plugin</a>

---

A simple poetry plugin that sets an environment variable containing the name of the current checked-out branch before executing any poetry command.

## Installation

Depending on how you installed poetry, there are different ways to install this plugin.

The easiest way to install this plugin is to use the `poetry self add` command:
```console
poetry self add poetry-git-branch-plugin
```

If you installed poetry using `pip`:
```console
pip install poetry-git-branch-plugin
```

If you installed poetry using `pipx`:
```console
pipx inject poetry poetry-git-branch-plugin
```

You can also specify that a plugin is required for your project in the
`tool.poetry.requires-plugins` section of the `pyproject.toml` file:
```yaml
[tool.poetry.requires-plugins]
poetry-git-branch-plugin = ">=0.0.1"
```

## Usage
Our main use case is in situations where DBT needs access to the current git branch name to set the name of the target schema.

## Contributing

[Poetry](https://python-poetry.org) is the best way to interact with this project, to install it,
follow the official [Poetry installation guide](https://python-poetry.org/docs/#installation).

With `poetry` installed, one can install the project dependencies with:

```shell
poetry install
```

Then, to run the project unit tests:

```shell
make test-unit
```

To run the linters (`ruff` and `mypy`):

```shell
make lint
```

To apply all code formatting:

```shell
make format
```

## License

`poetry-git-branch-plugin` is distributed under the terms of the
[MIT](https://opensource.org/license/mit) license.
Check the [LICENSE](./LICENSE) file for further details.
