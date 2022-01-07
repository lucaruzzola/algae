# pyfunds
Python Functional Data Structures

This repository contains an implementation from scratch of simple functional data structures in Python. 

The following structures are implemented and tested:
 - Either
 - Option
 - Try

This library is inspired by Scala's implementation of these structures.

Feel free to open an issue or [send me an email](mailto:lucaruzzola@gmail.com) 
in case you'd like to contribute or if you see something that can be improved.

## Usage Examples

### Either

`Either` represents a value that can assume one of two types.

Concrete instances are of type `Left` or `Right`.

### Option

`Option` represents an optional value, its concrete instances are 
of type `Nothing` or `Some`.

### Try

`Try` represents a computation that can either fail (raising an Exception) or return the resulting value.

Concrete instances are of type `Failure` or `Success`.

As an example, let's see the case of a function that can raise an Exception:
``` python
import math

def unsafe_computation(value: int):
    return math.log(value)  # this throws an Exception if value is <= 0
```

Upon calling this function with `value` <= 0 we'll see:

```python
unsafe_computation(0)
```
```shell
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: math domain error
```

To make this computation safe, even for `value` <= 0, we'll wrap its execution with Try:
```python
safe_result = Try.apply(unsafe_computation, 0)
```

`safe_result` will be of type `Failure`, containing the Exception.
In case it was called on proper input:
```python
safe_result = Try.apply(unsafe_computation, 1)
```

`safe_result` will be of type Success and it will contain the proper result.

Please notice that you need to pass the function and any function arguments, named and not, as arguments to 
`Try.apply()` rather than passing `f(args)`.

Alternatively, you can use this syntax:
```python
safe_result = Try.apply(lambda: unsafe_computation(0))
```

## Setup

### Poetry
This project uses [poetry](https://github.com/python-poetry/poetry) to manage its dependencies.
Please refer to [poetry's official doc](https://python-poetry.org/docs/) for more info.
