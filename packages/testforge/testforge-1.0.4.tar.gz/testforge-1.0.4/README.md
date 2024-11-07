# TestForge

**TestForge** A CLI tool to generate pytest test cases using AI.

## Features

- **Generate Tests**: Automatically generates pytest test cases for a specified file or function.
- **Output Directory**: Specify a custom output directory for the generated test files (default is the same as the file you're making tests for).
- **Configurable Endpoint**: Set an environment variable `TESTFORGE_INVITE` for the endpoint URL.

## Installation

Install TestForge via pip:

```bash
pip install testforge
```

## Usage

### Setting Up the Endpoint URL

TestForge requires an environment variable `TESTFORGE_INVITE` to get access to the beta. To set it up, use the following command:

```bash
export TESTFORGE_INVITE="YOURCODE"
```

Replace `YOURCODE` with the actual code you've received. This variable needs to be set in every session where you use TestForge or added to your shell configuration file (e.g., `.bashrc` or `.zshrc`) for persistence.

### Command Options

TestForge provides several options that can be used in the command line:

- **Show Version**: Check the version of TestForge.

  ```bash
  testforge -v
  ```

- **Generate Tests**: Generate pytest cases for a specified file.

  ```bash
  testforge -f path/to/your/file.py
  ```

- **Generate Tests for a function only**: Generate pytest cases for the specified function.

  ```bash
  testforge -f path/to/your/file.py -t function_name
  ```

- **Specify Output Directory**: Define a custom directory for the generated test files.
  ```bash
  testforge -f path/to/your/file.py -o path/to/your/custom_output_directory
  ```

## Example

```bash
export TESTFORGE_INVITE="INVITECODE"
testforge -f src/main.py -o tests
```
