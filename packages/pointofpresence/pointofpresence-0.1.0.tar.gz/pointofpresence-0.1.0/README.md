[![Contributor Covenant](https://img.shields.io/badge/code%20of%20conduct-Contributor%20Covenant-brightgreen.svg)](CODE_OF_CONDUCT.md)

# Point Of Presence Python Client Library

A Python client library for interacting with a specific POP API. This library provides easy-to-use methods for performing GET, POST, PUT, PATCH and DELETE requests, with built-in authentication support.

## Table of Contents

- [Installation](https://github.com/sci-ndp/pop-py/blob/main/README.md#installation)
- [Tutorial](https://github.com/sci-ndp/pop-py/blob/main/README.md#tutorial)
- [Running Tests](https://github.com/sci-ndp/pop-py/blob/main/README.md#running-tests)
- [Contributing](https://github.com/sci-ndp/pop-py/blob/main/README.md#contributing)
- [License](https://github.com/sci-ndp/pop-py/blob/main/README.md#license)

## Installation

Ensure you have Python 3.6 or higher installed. It's recommended to use a virtual environment.

### Option 1: Install from GitHub

1. **Clone the repository:**

   ```bash
   git clone https://github.com/sci-ndp/pop-py.git
   cd pop-py
   ```
2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install the package in editable mode:**

   ```bash
   pip install -e .
   ```
4. **Install development dependencies (optional, for testing):**

   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Install via pip

Once the package is published on PyPI, you can install it directly using pip:

```bash
pip install pointofpresence
```

## Tutorial

For a step-by-step guide on how to use the `pointofpresence` library, check out our comprehensive tutorial: [10 Minutes for a Point of Presence](https://github.com/sci-ndp/pop-py/blob/main/docs/point_of_presence_tutorial.ipynb).


## Running Tests

To run the tests, navigate to the project root and execute:

```bash
pytest
```

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a new branch** (`git checkout -b feature/new-feature`)
3. **Make your changes** and **commit** (`git commit -m 'Add new feature'`)
4. **Push** to the branch (`git push origin feature/new-feature`)
5. **Open a Pull Reques**

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/sci-ndp/pop-py/blob/main/LICENSE) file for details.
