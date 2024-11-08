# opPtimizer

Optimization framework for AI pipelines.

## Installation

### Install Opptimizer from PyPI
Appropriate for most use cases.

```
pip install opptimizer
```

## Examples of Usage
### Basic Pipeline Example

The following example demonstrates a simple pipeline that extends an input string by adding additional parts through modules `mod_1` and `mod_2`, ultimately returning the combined text.
```python
import opptimizer as op

def mod_1(mod_obj, params, tokenData = None):
    tokenData = tokenData + 'result 1'
    return tokenData

def mod_2(mod_obj, params, tokenData = None):
    tokenData = tokenData + ', result 2'
    mod_obj.setResult(tokenData)

executor = op.Executor(modules = [mod_1, mod_2])
response = executor.run('Results: ')

print(f"{response.get_result()}")
```

```markdown
Output:
    Results: result 1, result 2
```

## License

This project is licensed under the Apache License 2.0. You may use, modify, and distribute this software freely, provided that you comply with the terms of the license, which include attribution and a disclaimer of warranties. For the full license text, please see [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).