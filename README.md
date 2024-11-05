# Config2Code: A Tool to Generate Python Dataclasses from Configuration Files

![PyPI - Version](https://img.shields.io/pypi/v/config2class) ![PyPI - License](https://img.shields.io/pypi/l/config2class) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/config2class) [![Coverage Status](https://coveralls.io/repos/github/RobinU434/Config2Class/badge.svg)](https://coveralls.io/github/RobinU434/Config2Class)

## Introduction

Config2Code is a Python tool designed to streamline the process of converting configuration files (YAML or JSON or TOML) into Python dataclasses. By automating the generation of dataclasses, you can improve code readability, maintainability, and type safety.

## Installation

You can install Config2Code using pip:

```bash
pip install config2code
```

## Usage

You can either use the tool as a one time call or you could start a service which monitors your config file continuously.

### One time Call
1. **Prepare your configuration file:**
   Create a YAML or JSON file containing your configuration data. Here's an example YAML file:

   ```yaml
   database:
     host: localhost
     port: 5432
     user: myuser
     password: mypassword
   ```
2. **Run the tool:**
   Use the `config2code` command-line interface to convert the configuration file:

   ```bash
   config2code to-code --input input.yaml --output output.py
   ```

   This will generate a Python file `output.py` containing a dataclass representing the configuration:

   ```python
   from dataclasses import dataclass

   @dataclass
   class DatabaseConfig:
       host: str
       port: int
       user: str
       password: str
   ```

### Service
This service monitors the requested configuration file. If the services detects changes in the file it will automatically write those changes into the specified `output.py`.  
You can start the service for example with: 

```bash
config2code service-start --input input.yaml --output output.py
```

To stop it you can stop all with 

```bash
config2code stop-all
```

## Key Features

* **Supports YAML, JSON and TOML:** Easily convert both formats.
* **Automatic dataclass generation:** Generates well-structured dataclasses.
* **Nested configuration support:** Handles nested structures in your configuration files.
* **Type inference:** Infers types for fields based on their values.
* **Customizable output:** Control the output file name and code formatting.

## Additional Considerations

* **Complex data structures:** For more complex data structures, consider using custom type hints or additional configuration options.
* **Error handling:** The tool includes basic error handling for file loading and parsing.
* **Future enhancements:** We plan to add support for additional file formats, advanced type inference, and more customization options.

## Features to expand

* [ ] add VS Code extension (create new file on config file save)
* [ ] add renaming feature from config to code (renaming a field in the config file should resolve in renaming a field in the code
* [ ] add token in config yaml to overwrite field automatically with a dependency on another field (something like `<c2c/2*:dep.config.a/c2c>`) or costum functions `<c2c/module.submodule:func(some_value)/c2c>`

## Contributing

We welcome contributions to improve Config2Code. Feel free to fork the repository, make changes, and submit a pull request.

**License**

This project is licensed under the MIT License.
