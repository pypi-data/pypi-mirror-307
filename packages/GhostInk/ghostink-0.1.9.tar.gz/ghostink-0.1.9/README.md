# GhostInk

**GhostInk** is a Python utility to streamline debugging and etch(task) tracking by printing detailed file information for each call. This tool eliminates the need to manually add `print` statements and hunt for line numbers or file names, providing an organized, colorful output to track etches, debug info, and errors across your project.

---

## Installation

To install `GhostInk`, add it to your project with pip:

```bash
pip install ghosink
```

Then, import `GhostInk` into your Python files:

```python
from ghosink import GhostInk
```

---

## Usage

### Initialize GhostInk

To start, create a `GhostInk` instance with optional parameters:

```python
ink = GhostInk(
    title="My Project Debugger",
    project_root=".",         # Set the project root for relative path display
    log_to_file=True,         # Enable/disable logging to a file
    log_file="debug.log"      # Specify log file name if logging is enabled
)
```

### Adding etches (tasks) with Shades

Add etches with `inkdrop`, assigning Shades such as `TODO`, `INFO`, `DEBUG`, `WARN`, or `ERROR`. Shades allow you to manage and filter etches effectively.

```python
ink.inkdrop("Refactor this method", Shade=GhostInk.Shade.TODO)
# inkdrop can be aliased to just drop
ink.drop("This is debug info", Shade=GhostInk.Shade.DEBUG, echoes=["database"])
```

### Printing Location Information with `haunt`

If you simply want to print the current file location (file, line, function, and timestamp) without adding a etch, use `haunt`:

```python
# can be aliased to ink.ln()
ink.haunt("Executing important operation")
```

### Viewing and Filtering etches with `whisper`

View all tracked etches using `whisper`, with optional filters by Shade or file name:

```python
ink.whisper(shade_mask=GhostInk.Shade.TODO)
ink.whisper(file_mask="main.py")
ink.whisper(echo_mask=["database"])
```

---

## Key Methods

1. **`haunt(msg: str = None)`**  
   - Prints file, line, function, and timestamp for tracking execution points.
   - **Parameters**:
     - `msg`: Optional message displayed before the file information.

2. **`inkdrop(etch_input: any, Shade: Shade = Shade.TODO, echoes: List[str] = [])`**  
   - Adds a etch with text and a specific Shade to the etch list.
   - **Parameters**:
     - `etch_input`: Text, dictionary, or object to record as a etch.
     - `Shade`: etch Shade (TODO, INFO, DEBUG, WARN, ERROR).
     - `echoes`: Tags for the task

3. **`whisper(shade_mask: str = None, file_mask: str = None, echo_mask: List[str] = None)`**  
   - Prints filtered etches based on Shade and filename.
   - **Parameters**:
     - `shade_mask`: Filter etches by Shade.
     - `file_mask`: Filter etches by specific file name.
     - `echo_mask`: Filter etches by specific echo (Tag)

---

## Example

```python
from ghostink import GhostInk

ink = GhostInk(title="Project Debugger")
ink.drop("Fix memory leak", shade=GhostInk.Shade.WARN,
         echoes=['leaks', 'memory'])
ink.drop("Checkpoint reached", shade=GhostInk.Shade.INFO)
ink.drop("this is an importatnt TODO note DO NOT IGNORE")


ink.whisper(echo_mask=['memory'])

ink.haunt('just another line')

```

### Example Output

```bash
   Project Debugger

[WARN] Fix memory leak
Stack Trace:
  File "/home/yeeloman/Documents/GitHub/GhostInk_project/ghostink/main.py", line 4, in <module>
    ink.drop("Fix memory leak", shade=GhostInk.Shade.WARN,
  File "/home/yeeloman/Documents/GitHub/GhostInk_project/ghostink/ghostink.py", line 137, in inkdrop
    stack_trace = traceback.format_stack()

 #leaks   #memory
(Ln:4 - <module> in ghostink/main.py)

Printed from: ghostink/main.py at line 13
Review completed etchs and remove them as necessary.

just another line
└── main.py:15 in <module>() at 03:50:40``
```

---
## An import trick

 - to make `GhostInk` available in all file projects without the import statements, you can use `ghostall()`.
```python
# in a parentfile
from ghostink import ghostall
from subfile import buster
ghostall()

buster()
```
```python
# in a subfile
def buster():
  ink = GhostInk()
  ink.drop('now it work like a builtin function')
  ink.whisper()
``` 
---

## Benefits

- No more manually adding and searching for `print` statements!
- Clearly organized, color-coded outputs make etches easy to spot and review.
- Optional file logging to retain records and analyze later.
- Filters for viewing etches by file and Shade allow better focus and etch management.

---

**Start using GhostInk** and turn your debug prints into an organized, colorful log. Perfect for developers who want a better way to keep track of etches and debug information without losing context!

---

## Inspired By

This project is inspired by the [icecream](https://github.com/gruns/icecream) library.

---

## Contributing

Contributions are welcome! If you have suggestions or improvements, please create a pull request.
