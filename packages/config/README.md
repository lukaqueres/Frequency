# config

custom configuration module
___

- version `1.5.0`
- supports:
  - `json`
  - `yaml` _Requires PyYAML installed_

### Contains

- logging support with `config` logger set up.
- doctests in `doctest\doctests.txt`
___
## _Use_

Package must be imported from its location

```python
import config
```

### Loading:
- `dict`

  Module has method `config.save()` which adds passed `dict` to saved values
    ```python
    config.save({"name": "value"})
    ```
  It is used for saving parameters from files


- `json`
    
    Files require class `config.File`, which returns theirs contents in `dict` format.
    ```python
    config.save(config.File.json("doctest/doctests.json"))
    ```

- `yaml`
    
    Method `yaml` works similar to `json`, but requires yaml file instead of json.
    ```python
    config.save(config.File.yaml("doctest/doctests.yaml"))
    ```
  
  _**[Yaml support requires `PyYAML` package already installed](https://pypi.org/project/PyYAML/)**_
  
### Accessing:

- Saved values can be accessed by theirs name
    ```python
    config.get("name")
    ```
    If returned vale is not base ( not `int`, `str`, `list`, etc.), instance of `ResultSet` class will be returned instead.
    
    Values from them can be returned with 
    ```python
    config.get("nest").get("nested").get("more_nested")
    ```
    
- Getting raw values

    ```python
    config.raw()
    config.get("nest").raw()
    config.get("nest").get("nested").raw()
    ```
    If you need to get raw dict object instead of custom class instance, you can use `.raw()` method, 
    which can be found both in `config` and `ResultSet`

## Utils

- `logging`

  Logger used in package can be altered by fetching it from logging class

  ```python
  import logging
  logger = logging.getLogger('config')
  logger.setLevel(logging.DEBUG)
  ```
  By default, level is set to `INFO`

- `doctest`

  You can find `doctest` examples in `config\doctest\doctests.txt` along with example `yaml` and `json` files.

___
# _Changelog_

- `1.5.0`

  > Created `File` class with `json` and `yaml` methods
  > 
  > Data can now be saved from `yaml` files, and even raw `dict` with `config.save()`.
  >
  > Added `cnfig.dump()` method. It returns dict from saved values and removes them from memory.

- `1.0.0`

  > Added support for `json` files. 
  > 
  > Allowed accessing values with `get()` or `raw()` from `config` and `ResultSet` class
  > 
  > Data is now stored as static variables in package core.