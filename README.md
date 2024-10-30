**ig2Code: A Tool to Generate Python Dataclasses from Configuration Files**

**Introduction**

Config2Code is a Python tool designed to streamline the process of converting configuration files (YAML or JSON or TOML) into Python dataclasses. By automating the generation of dataclasses, you can improve code readability, maintainability, and type safety.

**Installation**

You can install Config2Code using pip:

```bash
pip install config2code
```

**Usage**

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
   config2code input.yaml output.py
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

**Key Features**

* **Supports YAML, JSON and TOML:** Easily convert both formats.
* **Automatic dataclass generation:** Generates well-structured dataclasses.
* **Nested configuration support:** Handles nested structures in your configuration files.
* **Type inference:** Infers types for fields based on their values.
* **Customizable output:** Control the output file name and code formatting.

**Additional Considerations**

* **Complex data structures:** For more complex data structures, consider using custom type hints or additional configuration options.
* **Error handling:** The tool includes basic error handling for file loading and parsing.
* **Future enhancements:** We plan to add support for additional file formats, advanced type inference, and more customization options.

**Contributing**

We welcome contributions to improve Config2Code. Feel free to fork the repository, make changes, and submit a pull request.

**License**

This project is licensed under the MIT License.
