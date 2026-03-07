import os
import pytest

from code2flow.model import Namespace, is_installed, djoin, flatten

def test_Namespace():
    name_space = Namespace("NAMESPACE1", "NAMESPACE2", "NAMESPACE3")
    assert name_space == {"NAMESPACE1": "NAMESPACE1", 
                          "NAMESPACE2": "NAMESPACE2", 
                          "NAMESPACE3": "NAMESPACE3"}

def test_Namespace_item():
    name_space = Namespace("NAMESPACE1", "NAMESPACE2")
    assert name_space.NAMESPACE2 == "NAMESPACE2"

def test_is_installed_dot():
    assert is_installed("dot.exe")

def test_is_installed_nonexistent():
    assert is_installed("nonexistent_command_12345") is False

def test_djoin():
    assert djoin((["A", "B", "C"])) == "A.B.C"

def test_djoin_items():
    assert djoin("A", "B", "C") == "A.B.C"

def test_flatten():
    assert flatten(["A", ["B", "C"], "D", None, []]) == ["A", "B", "C", "D"]