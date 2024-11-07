# PhoenixDataTools
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-python](https://img.shields.io/badge/Made%20with-PySpark-1f425f.svg)](https://www.python.org/)
[![for-use-in-Databricks](https://img.shields.io/badge/Made%20with-Databricks-1f425f.svg)](https://www.python.org/)

[![Documentation Status](https://readthedocs.org/projects/databricks-phoenixdatatools/badge/?version=latest)](https://databricks-phoenixdatatools.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/phoenixdatatools.svg)](https://badge.fury.io/py/phoenixdatatools)


PhoenixDataTools is a Python library specifically designed to optimize development in Databricks environments using PySpark. This library is ideal for integration into Databricks notebooks and jobs, offering a simplified and efficient interface for data manipulation.

The primary goal of PhoenixDataTools is to provide an abstraction layer that simplifies and accelerates working with small, medium, and large volumes of data, eliminating the need to write extensive lines of repetitive code. The library facilitates complex operations with DataFrames, Delta table manipulation, and management of storage and reading connections. This results in a significant improvement in productivity and code maintenance.

*******
Topics

1 - [Applied technologies](#tecnology)

2 - [Install library](#install)

3 - [Utilization](#utilization)

4 - [Library documentation](#docLib)

5 - [License](#license)

6 - [Local Development](#dev)

*******

<div id='tecnology'/> 

## Applied technologies

### [Poetry](https://python-poetry.org/)
Poetry is a dependency and package management tool for Python. It simplifies the creation, management, and publication of Python projects, ensuring a consistent development environment.

### [pytest](https://docs.pytest.org/en/stable/)
pytest is a powerful and flexible testing framework for Python. It makes writing simple and complex tests easy, allowing for robust and scalable test suites.

### [pytest-cov](https://pypi.org/project/pytest-cov/)
pytest-cov is a plugin for pytest that generates code coverage reports. It helps ensure that all parts of your code are tested by providing detailed coverage metrics.

### [taskipy](https://pypi.org/project/taskipy/)
taskipy is a tool that allows you to run scripts defined in `pyproject.toml`. It simplifies managing common project tasks by automating repetitive processes.

### [flake8](https://flake8.pycqa.org/en/latest/)
flake8 is a linting tool for Python that combines PyFlakes, pycodestyle, and mccabe. It checks your code for style errors and potential issues, helping maintain clean and consistent code.

### [isort](https://pycqa.github.io/isort/)
isort is a tool to automatically sort imports in your Python files. It organizes your imports according to style conventions, improving code readability and maintainability.

### [MkDocs](https://www.mkdocs.org/)
MkDocs is a static site generator geared towards project documentation. With it, you can create elegant and easy-to-navigate documentation websites from Markdown files.

### [Read the Docs](https://readthedocs.org/)
Read the Docs is a documentation hosting service that automates the building and versioning of your project's documentation. It integrates easily with code repositories, making documentation maintenance and access straightforward.


<div id='install'/> 

## Install library

You can install phoenixdatatools directly from PyPI by running the following command:

```sh

pip install phoenixdatatools

```
This will install the latest version of the library.


<div id='utilization'/> 

## Utilization

After installation, you can use the library directly in your code with the following syntax:

```sh

from phoenixdatatools import module

```

Each module provides specific functions relevant to its purpose. You can find detailed information about the available modules and functions in the following section: [Library Documentation](#library-documentation).

Example:

```sh
from phoenixdatatools import data_quality

data_quality.not_null_test(dataframe, columns)

```

<div id='docLib'/> 

## Library documentation

The library has comprehensive documentation covering all modules, usage instructions, and detailed examples. For complete information and guidance on how to use the library, visit our [official documentation on Read the Docs](https://databricks-phoenixdatatools.readthedocs.io/en/latest/).

<div id='license'/> 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for more details.


<div id='dev'/> 

## Local Development

For development and contribution to the project, access the [repository](https://bitbucket.org/indiciumtech/databricks-phoenixdatatools/src/main/) and go to section [Development](docs/templates/development.md)