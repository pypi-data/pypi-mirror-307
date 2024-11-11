# libManager

`libManager` is a Python class for managing project dependencies, including installation, information retrieval, dependency resolution, and creating a `requirements.txt` file.

## Overview

`libManager` simplifies dependency management in a project. This class enables:
- Checking installed libraries.
- Automatically installing required libraries.
- Automatically deleting libraries, **including their dependencies** _that **are not used** in **side-libraries**_.
- Retrieving information about libraries.
- Generating a `requirements.txt` file for dependency management.
- Installing/Deleting libraries based on `requirements.txt`

## Requirements

- Python 3.x
- `pip` package manager installed

***

## Installation

Download the library:

```bash
pip install libManager
```

Import the `libManager` class into your project.

```python
from lib_manager import libManager
```

***

## Usage

### 1. Initialization

Create an instance of the `libManager` class:

```python
manager = libManager()
```

Set target libraries manually:

```python
manager = libManager({"numpy", "pandas"})
```

Or set them via `requirements.txt`:

```Python
manager = libManager(path_to_requirements="D:\\Projects\\Default\\requirements.txt")
```

Or do both 😳:

```python
manager = libManager({"aiohttp"}, "D:\\Projects\\Telegram bot\\requirements.txt")
```

You can also manage to install all of the stated libraries at the beginning or not via `init_at_start` argument:

```python
#By default it is set to True
libManager(init_at_start = False)
```

### 2. Retrieving a Set of Installed Libraries

Use the `get_installed_libs` method to retrieve a list of installed libraries:

```python
installed_libs = manager.get_installed_libs()
```

### 3. Getting Details of The Library

If you need to get information about specific library from pip in convenient format, call the `get_lib_details` method:

```python
manager.get_lib_details("numpy")
```

This methods returns dictionary, containing the following keys of the library:
- name: str
- version: str
- summary: str
- home-page: str
- author: str
- author-email: str
- license: str
- location: str
- requires: set[str]
- required-by: set[str]

### 4. Getting All Dependencies of The Library

If you need to get all libraries that are being used in the library, call the `get_all_dependencies` method:

```python
dependencies: set[str] = manager.get_all_dependencies("numpy")
```

**It should be noted that this information depends on the result of 'pip show' command.**
**If dependencies are not stated in pip, the function will return an empty set**

### 5. Installing Libraries

To install a set of required libraries, call the following method:

```python
manager.init_libs()
```

### 6. Deleting Libraries

To delete all of the libraries that are stated `libraries_needed`, **including their dependencies**, call the `deinit_libs` method:

```python
#Initialize libraries we need
manager = libManager({'numpy', 'pandas'})
import numpy
import pandas

#Work goes here

#Shall we clean up after hard work?
manager.deinit_libs()
```

**It should be noted that it deletes only those libraries that are not used in other side-libraries**.

### 7. Creating a requirements.txt File

To create a `requirements.txt` file, use `create_actual_requirements`:

```python
manager = libManager()

manager.create_actual_requirements("*path_to_file*.py")
```

Thus, `libManager` will try to create `requirements.txt` based only on your project file.

However, if there are libraries that practically can not be got from the file, you can directly state them in `additional_libs` argument:

```python
manager.create_actual_requirements("*path_to_file,py*", additional_libs={"aiohttp"})
```

### 8. Getting Libraries From requirements.txt File

To get libraries from `requirements.txt`, call `add_libs_from_requirements` method:

```python
manager.add_libs_from_requirements("D:\\Projects\\Hard project\\requirements.txt")
```

**It has to be noted that libManager only recognises file with the appropriate name.**

### 9. Deleting Libraries From libManager by requirements.txt File

If at some point you want to stop working with libraries from `requirements.txt`, remove them via `remove_libs_by_requirements` method

```python
manager.remove_libs_by_requirements("D:\\Projects\\Hard project\\requirements.txt")
```

***
## Methods
- `get_installed_libs`: Returns a set of installed libraries. Can focribly get update of installed libraries via setting `update` argument to `True`
- `get_lib_details`: Returns a dictionary with information about specific library. Information can also be found in pip via `pip show [library_name]` command
- `get_all_dependencies`: Recursively returns a set of libraries that are needed for specific library to run. It can take a plenty of time.
- `create_actual_requirements`: Creates a requirements.txt file basing on target `file.py`.
- `add_libs_from_requirements`: Adds libraries to `libManager` from `requirements.txt`.
- `remove_libs_by_requirements`: Removes libraries from `libManager` basing on `requirements.txt`
- `init_libs`: Installs specified libraries basing on `libraries_needed`.
- `deinit_libs`: Delets specified libraries **and their dependencies** basing on `libraries_needed`

## License
#### This project is licensed under the MIT License.