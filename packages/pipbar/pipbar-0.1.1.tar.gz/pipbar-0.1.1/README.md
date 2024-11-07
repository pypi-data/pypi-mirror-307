```c
┏┓┳┏┓  ┳┓┏┓┳┓
┃┃┃┃┃  ┣┫┣┫┣┫
┣┛┻┣┛  ┻┛┛┗┛┗
```

`pipbar` is a Python tool that shows a progress bar with ETA and download speed when installing packages using `pip`. It enhances the user experience by displaying a progress bar during installation, making it easy to track the progress and estimated time for completion.

## Features

- Displays a progress bar for `pip` installations
- Shows the ETA (estimated time of arrival) and download speed
- Provides user-friendly messages and status updates during package installation
- Open-source and easy to use

## Installation

You can install `pipbar` directly from PyPI using `pip`:

```bash
pip install pipbar
```


PyPl: [https://pypi.org/project/pipbar/0.1.0/](https://pypi.org/project/pipbar/0.1.0/)

## Usage

Once `pipbar` is installed, you can use it to install packages with a progress bar.

### Install a Single Package

Here’s an example of how to install a package (e.g., `requests`) using `pipbar`:

```python
from pipbar import install_package

install_package("requests")
```

This will install the `requests` package and show a progress bar with the ETA and download speed.

### Install Multiple Packages

You can also install multiple packages at once by using the `install_packages` function:

```python
from pipbar import install_packages

install_packages(["requests", "numpy", "pandas"])
```

This will install `requests`, `numpy`, and `pandas` with a progress bar for each package.

## License

`pipbar` is an open-source project released under the **MIT License**.

