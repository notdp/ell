import pytest
import math
from typing import Set, Any
import numpy as np
from ell.util.closure import (
    lexical_closure,
    is_immutable_variable,
    should_import,
    get_referenced_names,
    is_function_called,
)

def test_lexical_closure_simple_function():
    def simple_func(x):
        return x * 2

    result, (source, dsrc), uses = lexical_closure(simple_func)
    assert "def simple_func(x):" in result
    assert "return x * 2" in result
    assert isinstance(uses, Set)

def test_lexical_closure_with_global():
    global_var = 10
    def func_with_global():
        return global_var

    result, _, _ = lexical_closure(func_with_global)
    assert "global_var = 10" in result
    assert "def func_with_global():" in result

def test_lexical_closure_with_nested_function():
    def outer():
        def inner():
            return 42
        return inner()

    result, _, _ = lexical_closure(outer)
    assert "def outer():" in result
    assert "def inner():" in result
    assert "return 42" in result

def test_lexical_closure_with_default_args():
    def func_with_default(x=10):
        return x

    result, _, _ = lexical_closure(func_with_default)
    print(result)
    assert "def func_with_default(x=10):" in result

@pytest.mark.parametrize("value, expected", [
    (42, True),
    ("string", True),
    ((1, 2, 3), True),
    ([1, 2, 3], False),
    ({"a": 1}, False),
])
def test_is_immutable_variable(value, expected):
    assert is_immutable_variable(value) == expected

def test_should_import():
    import os
    assert should_import(os)
    
    class DummyModule:
        __name__ = "dummy"
    dummy = DummyModule()
    assert not should_import(dummy)

def test_get_referenced_names():
    code = """
    import math
    result = math.sin(x) + math.cos(y)
    """
    referenced = get_referenced_names(code, "math")
    print(referenced)
    assert "sin" in referenced
    assert "cos" in referenced

def test_is_function_called():
    code = """
def foo():
    pass

def bar():
    foo()

x = 1 + 2
    """
    assert is_function_called("foo", code)
    assert not is_function_called("bar", code)
    assert not is_function_called("nonexistent", code)

# Addressing linter errors
def test_lexical_closure_signature():
    def dummy_func():
        pass

    # Test that the function accepts None for these arguments
    result, _, _ = lexical_closure(dummy_func, already_closed=None, recursion_stack=None)
    assert result  # Just check that it doesn't raise an exception

def test_lexical_closure_uses_type():
    def dummy_func():
        pass

    _, _, uses = lexical_closure(dummy_func, initial_call=True)
    assert isinstance(uses, Set)
    # You might want to add a more specific check for the content of 'uses'