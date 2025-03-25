# Config2Class: A Tool to Generate Python Dataclasses from Configuration Files

![PyPI - Version](https://img.shields.io/pypi/v/config2class) ![PyPI - License](https://img.shields.io/pypi/l/config2class) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/config2class) [![Coverage Status](https://coveralls.io/repos/github/RobinU434/Config2Class/badge.svg)](https://coveralls.io/github/RobinU434/Config2Class) ![PyPI - Downloads](https://img.shields.io/pypi/dm/config2class)

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
   DatabaseConfig:
     host: localhost
     port: 5432
     user: myuser
     password: mypassword
   ```
2. **Run the tool:**
   Use the `config2code` command-line interface to convert the configuration file:

   ```bash
   c2c file2code --input input.yaml --output output.py
   ```

   This will generate a Python file `output.py` containing a dataclass representing the configuration:

   ```python
   from dataclasses import dataclass
   from config2class.api.base import StructuredConfig

   @dataclass
   class DatabaseConfig(StructuredConfig):
       host: str
       port: int
       user: str
       password: str
   ```

### file2code

As shown in the previous example `file2code` is only concerned with mapping one given config file of any type into a structured python. Explore options within this command with: `c2c file2code --help`

### dir2code

This command is an aggregation of `file2code`. With `dir2code` you point to a directory where multiple config files are saved mark an output directory where you would like to write the python files each with structured configs per file inside.

### hydra2code

This command enables to write your structured-config from hydra config from a single config file or distributed over multiple config files. This command uses the `hydra.compose` api to load the specified config files.

### Placeholder Example

Sometimes you put redundant data in your config file because it is more convenient to only move parts of the config further down the road. Examples could be a machine learning pipeline where you have parameters for your dataset and model which can have redundant values. To counter the problem of always changing multiple values at once in your config we introduce **placeholder**.  A placeholder is a path packed into a token `${<path-in-config>}` which points to a value you want to insert automatically into your loaded config file. This path starts always at the yaml root and ends at the value to insert.

```yaml
   pipeline:
      dataset: 
         x_dim: 42
         y_dim: 5
         batch_size: 128
         shuffle: True
      model:
         input_dim: ${pipeline.dataset.x_dim}
         output_dim: ${pipeline.dataset.y_dim}
         activation_func: ReLU
         learning_rate: 0.0001
```

Here we use the API of [OmegaConf](https://omegaconf.readthedocs.io/en/2.3_branch/). Therefor you are allowed to use all kinds of funny stuff like custom evaluators or missing value imputation or merging config files from multiple files or .... .
Please note for the last one is no tested feature for merging configs from multiple files into one big structured config.

### Service

> **_Note:_** Please note this feature is still underdevelopment under the new API. There can be unforeseen behavior with this command. Please be careful

This service monitors the requested configuration file. If the services detects changes in the file it will automatically write those changes into the specified `output.py`.
You can start the service for example with:

```bash
config2code service-start --input input.yaml --output output.py
```

To stop it you can stop all with

```bash
config2code stop-all
```

### Use Config in Code

After you created your python config you can easily use as follows:

```python
from output import DatabaseConfig

config = DatabaseConfig.from_file("input.yaml")
# access config field with dot operator
config.host
```

This is different to a normal `DictConfig` from OmegaConf because this supports code completion in your coding environment.

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

## Contributing

We welcome contributions to improve Config2Code. Feel free to fork the repository, make changes, and submit a pull request.

**License**

This project is licensed under the MIT License.
