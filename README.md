# CVPython

> Small, readable Python implementations to learn **Computer Vision** by doing.

CVPython is an educational collection about Computer Vision. Each **concept** comes with
a short theory write-up and a working demo, so you can read *why* something works
and then run the code to see it in action. 

Alongside the concepts, a set of **tools**
shows how those ideas are applied to solve real tasks.

This is **not** a library or an application: there is nothing to import or install
as a package. It is meant to be read, run, modified and broken.

## Contents

- [Repository structure](#repository-structure)
- [Concepts](#concepts)
- [Tools](#tools)
- [Getting started](#getting-started)
- [How to use this repository](#how-to-use-this-repository)
- [Disclaimer](#disclaimer)


## Repository structure

```
CVPython/
├── README.md
├── pyproject.toml          # dependencies (uv)
├── uv.lock                 # pinned versions
├── requirements.txt        # pip fallback, exported from uv
├── data/                   # datasets / sample data (ignored by git)
├── concepts/
│   ├── 01_<subdomain>/
│   │   ├── README.md       # overview + index of this subdomain
│   │   ├── <concept>.md    # theory
│   │   ├── <concept>.py    # demo (or .ipynb)
│   │   └── assets/         # images and diagrams
│   └── 02_<subdomain>/
└── tools/
    └── <tool_name>/
        ├── README.md       # what it does and how to run it
        └── main.py
```

- **`concepts/`** — Theory and demos, grouped by subdomain and numbered in a
  suggested reading order. Each subdomain has its own `README.md` with an
  overview and an index of the concepts it contains.
- **`tools/`** — Complete, functional programs that apply the concepts to a
  specific task. More robust than the demos, and ***closer*** to a real-world
  implementation.

## Concepts

## Tools

## Getting started

### Requirements

- Python >= 3.14
- [uv](https://docs.astral.sh/uv/) (recommended) or `pip`

### Option A — uv (recommended)

```bash
git clone https://github.com/PabloFl07/CVPython.git && cd CVPython
uv sync
```

`uv sync` creates a virtual environment and installs the exact versions pinned
in `uv.lock`, so every demo runs the same way it did when it was written.

### Option B — pip

```bash
git clone https://github.com/PabloFl07/CVPython.git && cd CVPython
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## How to use this repository

### 1. Read the theory, then run the demo

Pick a subdomain in [Concepts](#concepts) and open its `README.md` for the
overview. Each concept is a pair of files with the same name:

- `<concept>.md` — the theory: what it is, why it works, where it is used.
- `<concept>.py` or `<concept>.ipynb` — a demo that puts the theory into practice.

```bash
uv run concepts/01_<subdomain>/<concept>.py
# or, with pip and the virtual environment activated:
python concepts/01_<subdomain>/<concept>.py
```

### 2. Open the notebooks

I will be using 2 types of notebooks:

- **Marimo Notebooks**: they are generated from a Python file and arranged into a Notebook in a local server.
They are aeasier to versionate and use outside of a notebook interpreter.

```bash
marimo edit file.py   # The notebook will behave like a Jupyter Notebook

marimo run file.py    # It just runs the cells and shows the output
```
Tutorial on Marimo's main features coming soon.

- **Jupyter Notebooks**: they keep their outputs, so you can read them directly on GitHub without
running anything. However, they may be heavier and need the Jupyter Server.

```bash
uv run --with jupyter jupyter lab
```
This will start a Jupyter Notebooks session on your **browser**

> [!NOTE]
> `uv run --with jupyter` downloads Jupyter and its dependencies the first time you run it.
> They are **not** added to the project: `pyproject.toml`, `uv.lock` and `.venv` stay untouched.
> uv installs them into a temporary environment and keeps them in its global cache,
> so later runs start almost instantly. To free that space, run `uv cache clean`.


### 3. Try the tools

Each tool has its own `README.md` with usage instructions and examples.
Tools declare their own dependencies in an inline header (PEP 723), so they can
be run on their own, even if copied out of the repository:

```bash
uv run tools/<tool_name>/main.py --help
```

### 4. Experiment

The demos are deliberately small. Change parameters, feed them different
inputs, break them and see what happens: that is the point.

## Disclaimer

**Educational use only.** The code in this repository is written for clarity,
not for production. It has not been audited and may omit checks, optimizations
or edge cases that real systems need. For real-world work, use well-established
libraries and follow industry best practices.
