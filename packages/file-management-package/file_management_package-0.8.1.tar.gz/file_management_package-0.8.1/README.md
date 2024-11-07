# File Management Package

`file-management-package` is a Python package designed to simplify file management tasks. It provides a convenient set of tools to create, read, write, delete, and manage files in a system, while handling common errors and ensuring robust functionality.

# Features

- **File Writing**: Write to a file, either appending or writing a single line.
- **File Reading**: Read a file either line by line or as a whole.
- **File Existence Check**: Check if a file exists.
- **File Creation**: Automatically create a file if it doesn't exist.
- **File Deletion**: Delete a file from the system.
- **File Content Modification**: Remove specific content from a file.
- **File Opening**: Open files using the default application for the file type.

# Installation

To install the package, use the following command:

```bash
pip install file-management-package
```
Or put in your `requirements.txt`

```txt
file-management-package==0.8.1
```

# Usage
## Importing the Package
To use the FileManagement class, import it into your project as follows:

``` python
from file_management_package.file_management import FileManagement
```

## Example Usage
1. Writing to a File:

``` python
fm = FileManagement()
fm.write_to_file("Hello, world!", "example.txt")
```
This will write "Hello, world!" to the file example.txt, creating the file if it does not exist.

If you want a custom file location you need to do this
``` python
fm = FileManagement(base_directory="path/to/your/folder")
```

2. ### Reading a File Line by Line:

```python
lines = fm.read_file_per_line("example.txt")
print(lines)
```

This will read the contents of `example.txt` and return a list of lines.

3. ### Check if a File Exists:

```python
file_exists = fm.check_if_file_exists("example.txt")
print(file_exists)  # Output: True or False
```

4. ### Create a New File:

```python
fm.create_file("new_file.txt")
```

5. ### Delete a File:

```python
fm.delete_file("example.txt")
```

6. ### Remove Specific Content from a File:

```python
fm.delete_from_file("example.txt", "Hello")
```

This will remove all lines in `example.txt` that contain the word "Hello".

7. ### Open a File:

```python
fm.open_file("example.txt", is_sdk=False)
```

This will open `example.txt` with the default file handler (e.g., Notepad, TextEdit, etc.).

# Error Handling

The `FileManagement` class includes robust error handling for:

- `FileNotFoundError`: If the file is not found.
- `PermissionError`: If there are permission issues.
- `IOError`: General I/O issues with the file system.
- General exceptions are caught and handled gracefully.

# License
This package is licensed under the MIT License. See the LICENSE file for more details.

# Author
Created by Pascal Benink. You can reach me at 2sam2samb+PythonFile@gmail.com.
