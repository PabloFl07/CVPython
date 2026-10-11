# Contribution Guide

This guide explains how I worked for this project.

## Index

- [Setup](#setup)
- [Workflow](#workflow)
- [Commits](#commits)
- [Branch model](#branch-model)
- [Style guide](#style-guide)
- [Documentation](#documentation)


## Setup

The only tools you need are [Git](https://git-scm.com/) and [uv](https://docs.astral.sh/uv/).
uv installs the right Python version and all project dependencies for you, so there is no need to install Python manually or use pip.
All dependencies are listed in `pyproject.toml`.

> [!NOTE]
> If you cannot use uv, a `requirements.txt` file is also provided as an alternative.

```bash
git clone https://github.com/PabloFl07/CVPython.git && cd CVPython
uv sync
uv run pre-commit install
uv run CVPython
```

## Workflow

#### Notes
- Correct [commit messages](#commits) and [branch names](#branch-model)
- What is allowed to commit: [What not to commit](#what-not-to-commit)

**1. Create a new branch based on `dev`**

```bash
git switch dev
git pull
git switch -c correctly-named-branch
```

**2. Work on it and push it**

```bash
git add ...
git commit -m "correctly redacted commit message"
git push -u correctly-named-branch
```

**3. Switch to dev and merge your branch**

```bash
git switch dev && git pull
git merge correctly-named-branch
git push
```

## Commits

We follow [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/):

```
<type>(<optional scope>): <description>

[optional body]

[optional footer]
```

- The description must be written in the imperative, without a period, and no more than 72 characters long.
- The `scope` is optional. If you include it, use the name of the affected module (`import`, `gui`, `model`, `storage`, etc.).

|Type|When|
|---|---|
|`feat`|	Adds a new feature or capability for the user, such as a new screen, option, command or supported input.
|`fix`|	Fixes a bug, meaning behavior that didn’t match what was expected. Includes crashes, wrong results and unhandled edge cases.
|`docs`|	Changes only documentation: README, docstrings, code comments, guides or usage examples. No code behavior changes.
|`refactor`|	Restructures or cleans up code without changing what it does: renaming, splitting functions, moving files or removing duplication.
|`test`|	Adds new tests, or fixes or updates existing ones, without touching production code.
|`build`|  Changes the build system or dependencies: adding, removing or upgrading packages, editing pyproject.toml, the uv lockfile or packaging settings.
|`ci`|	Changes continuous integration configuration, such as GitHub Actions workflows that run tests, linters or deployments automatically.
|`chore`|	Routine maintenance that doesn’t affect the code’s behavior and doesn’t fit any other type, such as updating .gitignore, editor config or repository housekeeping.


> [!Tip]
> Append ! after the type/scope when the commit introduces a `BREAKING CHANGE`

## Branch Model

| Branch | Usage |
|---|---|
| `main` | Released versions only.  |
| `dev` | Integration of finished work **via merge exclusively**.  |
| `feature/<nº>-<description>` | One branch per user story or task.  |
| `fix/<nº>-<description>` | Any fix applied in the proyect.  |
| `docs/<description>` | Documentation changes or additions.|

`main` contains only stable versions and only receives changes from `dev` via merge

`dev` branches off `main` and is merged back into `main`

`type branches` branch off `dev` and are merged back into `dev` upon completion of a history or task.

## Style guide

All code must follow Python's [PEP 8](https://peps.python.org/pep-0008/) style guide. We enforce it with [Ruff](https://docs.astral.sh/ruff/), which acts as both linter and formatter. Its configuration lives in `pyproject.toml`.

You can check and format your coude manually:

```bash
uv run ruff format .        # format the code
uv run ruff check . --fix   # lint and fix what can be fixed automatically
```
However, there are pre-commit hooks configured that run these checks automatically.

#### Additional conventions

- **Naming:** `snake_case` for variables, functions and modules; `PascalCase` for classes; `UPPER_CASE` for constants.
- Add **Type hints:**  to every public function's parameters and return value.
- **Docstrings:** every public module, class and function must have one.
- **Imports:** grouped as standard library, third-party and local, in that order. Ruff sorts them automatically.
- **Language:** code, comments and docstrings are written in English.

## Documentation

- `README.md`: basic information about the project. You may not modify it
- `docs/`: detailed documentation (architecture, design decisions, user manual)
- `CHANGELOG.md`: brief description of the changes in each version

