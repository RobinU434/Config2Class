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

### Hydra Integration

Additionally we support now a Hydra integration where provide functions to add the hydra ArgumentParser to your custom parser.
> **_Note:_** Please note this feature is still underdevelopment. Therefor please be careful while merging those two argument parser and setup the wrapper function. A rough example can be examined [here](usage_examples/hydra_integration.py)

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
* [ ] add renaming feature from config to code (renaming a field in the config file should resolve in renaming a field in the code
* [ ] expand token feature so you can access memeber of a list `{{<path>.<to>.<element>[<index>]}}`

## Contributing

We welcome contributions to improve Config2Code. Feel free to fork the repository, make changes, and submit a pull request.

**License**

This project is licensed under the MIT License.
