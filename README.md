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

### Basic Example

1. **Prepare your configuration file:**
   Create a YAML or JSON file containing your configuration data. Here's an example YAML file:

   ```yaml
   database:
     host: localhost
     port: 5432
     user: myuser
     password: mypassword
     secret: {{database.password}}
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
       secret: str
   ```

#### Placeholder Example

Sometimes you put redundant data in your config file because it is more convenient to only move parts of the config further down the road. Examples could be a machine learning pipeline where you have parameters for your dataset and model which can have redundant values. To counter the problem of always changing multiple values at once in your config we introduce **placeholder**.  A placeholder is a path packed into a token `{{<path-in-config>}}` which points to a value you want to insert automatically into your loaded config file. This path starts always at the yaml root and ends at the value to insert. 

```yaml
   pipeline:
      dataset: 
         x_dim: 42
         y_dim: 5
         batch_size: 128
         shuffle: True
      model:
         input_dim: {{pipeline.dataset.x_dim}}
         output_dim: {{pipeline.dataset.y_dim}}
         activation_func: ReLU
         learning_rate: 0.0001
```

In the case of not having a yaml root you can still use the placeholder with a leading `.` inside the token. 


```yaml
   dataset: 
      x_dim: 42
      y_dim: 5
      batch_size: 128
      shuffle: True
   model:
      input_dim: {{.dataset.x_dim}}
      output_dim: {{.dataset.y_dim}}
      activation_func: ReLU
      learning_rate: 0.0001
```


## Key Features

* **Supports YAML, JSON and TOML:** Easily convert both formats.
* **Automatic dataclass generation:** Generates well-structured dataclasses.
* **Nested configuration support:** Handles nested structures in your configuration files.
* **Type inference:** Infers types for fields based on their values.
* **Placeholder:** Choose which values in your config file are dependent on others

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
