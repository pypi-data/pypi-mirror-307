# Poetry Shared Venv Plugin

## SonarCloud Status

[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_poetry-shared-venv-plugin&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_poetry-shared-venv-plugin)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_poetry-shared-venv-plugin&metric=bugs)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_poetry-shared-venv-plugin)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_poetry-shared-venv-plugin&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_poetry-shared-venv-plugin)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_poetry-shared-venv-plugin&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_poetry-shared-venv-plugin)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_poetry-shared-venv-plugin&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_poetry-shared-venv-plugin)

[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_poetry-shared-venv-plugin&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_poetry-shared-venv-plugin)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_poetry-shared-venv-plugin&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_poetry-shared-venv-plugin)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_poetry-shared-venv-plugin&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_poetry-shared-venv-plugin)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_poetry-shared-venv-plugin&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_poetry-shared-venv-plugin)

Centralize your monorepo submodules in a single virtual environment.

## Motivation

In a monorepo-style project with multiple poetry projects in the same repository, and each project has its own virtual environment, installing dependencies can be a time-consuming task, especially when the dependencies are shared among the projects.

The IDEs also have a hard time switching between them as you navigate through the codebase.

This plugin aims to solve this problem by centralizing the virtual environments in a single directory, very similar to how `yarn workspaces` works.

## Install

`poetry self add poetry-shared-venv-plugin`

## Usage

1. Create a `pyproject.toml` file in the root of your repository.
2. Add the `shared-venv` section to the `pyproject.toml` file.

```toml
[tool.poetry]
name = "demo"
version = "0.1.0"
description = "Python workspace"
authors = []
package-mode = false

[tool.poetry.dependencies]
python = "^3.12"

[tool.shared-venv]
enabled = true
root = true
include = [
    "packages/**"
]
```

3\. Add your packages to the `packages` directory. (or any other directory you want)

Now, when you run the poetry commands to add, update or remove the dependencies, the plugin will install them in the shared virtual environment in the root of the repository, but it will still generate the `poetry.lock` file in the package directory as usual.

The root `poetry.lock` file will be generated in the root of the repository.

## Contributing

- See our [Contributing Guide](CONTRIBUTING.md)

## Change Log

- See our [Change Log](CHANGELOG.md)
