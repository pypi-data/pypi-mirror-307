# HissCL

A [HashiCorp Config Language](https://github.com/hashicorp/hcl) parser for Python

## Usage

For most simple use-cases, you can use the `load*` convenience functions:

`load_file()`:
```python
import hisscl
cfg = hisscl.load_file("config.hcl")
```

`loads()`:
```python
import hisscl
# Use the optional name argument to specify a filename for errors
cfg = hisscl.loads("x = 2 * 4", name='string.hcl')
```

`load()`:
```python
import hisscl
with open('test.hcl', 'r') as fl:
    # Use the optional name argument to specify a filename for errors
    cfg = hisscl.load(fl, name=fl.name)
```

Each `load*` function has an optional `vars: dict[str, Any]` parameter, whose elements are used as variables in your config file. For example, if you have `x = y + 1`, `y` must be defined in `globals`.

For more advanced use-cases, `lexer`, `parser`, `ast`, and `interp` submodules are provided.

## Output Format

The interpreter outputs a python dictionary containing field values and blocks. Blocks are stored in a list of `interp.Block` values. `interp.Block` is a subclass of `dict` with an extra `labels` attribute that can be used to get a list of block labels. For example:

```python
import hisscl
cfg = hisscl.loads('x "y" "z" { a = "b" }')
print(cfg['x'][0].labels) # ['y', 'z']
print(cfg['x'][0]['a']) # b
```

## Features

Currently, this parser supports all HCL features except:

- [For Expressions](https://github.com/hashicorp/hcl/blob/main/hclsyntax/spec.md#for-expressions)
- [Templates](https://github.com/hashicorp/hcl/blob/main/hclsyntax/spec.md#templates)
- [Function Calls](https://github.com/hashicorp/hcl/blob/main/hclsyntax/spec.md#functions-and-function-calls)

Support for these features is planned.