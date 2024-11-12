# jupyter_ai_wekeo

`jupyter_ai_wekeo` is a Jupyter AI module, a package
that registers additional model providers and slash commands for the Jupyter AI
extension.

## Requirements

- Python 3.8 - 3.12
- JupyterLab 4

## Install

To install the extension, execute:

```bash
pip install jupyter-ai-wekeo
```

## Uninstall

To remove the extension, execute:

```bash
pip uninstall jupyter-ai-wekeo
```

## Contributing

### Development install

```bash
cd jupyter-ai-wekeo
pip install -e "."
```

### Development uninstall

```bash
pip uninstall jupyter-ai-wekeo
```

#### Backend tests

This package uses [Pytest](https://docs.pytest.org/) for Python testing.

Install test dependencies (needed only once):

```sh
cd jupyter-ai-wekeo
pip install -e ".[test]"
```

To execute them, run:

```sh
pytest -vv -r ap --cov jupyter-ai-wekeo
```
