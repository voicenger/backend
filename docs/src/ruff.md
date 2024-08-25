# Code Linting with Ruff

## Overview

`Ruff` is a fast and powerful linter for Python, designed to enforce coding standards and improve code quality. 
It supports various linting rules and can be integrated into your development workflow to catch issues early.

This project uses `Ruff` to automatically check and enforce code quality standards, including:

- **Unused imports and variables**: Identifies and removes any unused imports or variables in the code.
- **Code style violations**: Ensures adherence to code style guidelines such as PEP 8.
- **Potential bugs**: Detects potential bugs and logical errors in the code.


## Configuration

`Ruff` is configured using a `ruff.toml` file located in the root directory of the project. 
This file specifies which linting checks to enable and how they should be applied. 
The configuration can be customized to fit the project's needs and may include:

- **Style Checks**: Enforce consistent code style according to PEP 8 and other style guides. For example, checking for proper use of quotes and enforcing naming conventions.

- **Code Quality Checks**: Identify potential issues in the code, such as unused imports, variables, and function arguments. This helps to maintain code quality and prevent bugs.

- **Best Practices**: Ensure adherence to best practices in Python development,such as avoiding print statements and using proper exception handling.

## Usage
To run Ruff on your project and ensure code quality, follow these steps:

### 1. Install Ruff
Ensure that Ruff is installed in your environment. If Ruff is listed in your `requirements-dev.txt`, install it along with other development dependencies using:

**Via `requirements-dev.txt`:**
Make sure ruff is included in your requirements-dev.txt. If it is, you can install it by running:

```bash
pip install -r requirements-dev.txt
```
Alternatively, you can install Ruff directly using pip:

```bash
pip install ruff
```

### 2. Run Ruff
**Lint all files**. This command will check all Python files in the current directory and its subdirectories.
```bash
ruff check .
```
**Automatically fix issues**. To automatically fix issues where possible, use:
```bash
ruff --fix .
```
**Watch for changes**. To lint all files and re-lint on changes, use:
```bash
ruff check --watch
```
**Check or fix specific files/directories** .Replace path/to/file.py or path/to/code/ with the path to the file or directory:
```bash
ruff check path/to/file.py
ruff check --fix path/to/file.py
ruff check path/to/code/
ruff check --fix path/to/code/
```
### 3. Format Code

**Format all files**. To format all files in the current directory:
```bash
ruff format
```
**Format files in a specific directory**. To format all files in a specific directory (and its subdirectories):

```bash
ruff format path/to/code/
```
**Format a single file**. To format a single file:
```bash
ruff format path/to/file.py
```

### Resources and Documentation

For more detailed information about `Ruff` and its capabilities, check out the following resources:

- **Official Documentation**: Refer to the [official Ruff documentation](https://docs.astral.sh/ruff/) for in-depth guidance and examples.














