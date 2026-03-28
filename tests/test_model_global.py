import os
import pytest

from code2flow.model import Namespace, is_installed, djoin, flatten
from code2flow.model import _resolve_str_variable, _wrap_as_variables
from code2flow.model import Group, Node, Variable, GROUP_TYPE, OWNER_CONST

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

def test_flatten_empty():
    assert flatten([]) == []
    assert flatten([[], None]) == []

def test__resolve_str_variable_node():    
    group1 = Group('myfile.py', 'FILE', 'File')
    node1_1 = Node('node1_1', None, None, group1, import_tokens=["node1_1"])
    node1_2 = Node('node1_2', None, None, group1, import_tokens=["node1_2"])
    group1.add_node(node1_1)
    group1.add_node(node1_2)
    
    group2 = Group('myclass.py', 'CLASS', 'Class')
    node2_1 = Node('node2_1', None, None, group2, import_tokens=["node2_1"])
    node2_2 = Node('node2_2', None, None, group2, import_tokens=["node2_2"])
    group2.add_node(node2_1)
    group2.add_node(node2_2)

    file_groups = [group1, group2]

    var = Variable("var1", "node1_1")

    resolved = _resolve_str_variable(var, file_groups)
    assert resolved == node1_1


def test__resolve_str_variable_group():    
    group1 = Group('myfile.py', 'FILE', 'File')
    group1_1 = Group('group1_1', "FILE", "File", import_tokens=["group1_1"])
    group1_2 = Group('group1_2', "FILE", "File", import_tokens=["group1_2"])
    group1.add_subgroup(group1_1)
    group1.add_subgroup(group1_2)
    
    group2 = Group('myclass.py', 'CLASS', 'Class')
    group2_1 = Group('group2_1', "CLASS", "Class", import_tokens=["group2_1"])
    group2_2 = Group('group2_2', "CLASS", "Class", import_tokens=["group2_2"])
    group2.add_subgroup(group2_1)
    group2.add_subgroup(group2_2)

    file_groups = [group1, group2]

    var = Variable("var1", "group1_1")

    resolved = _resolve_str_variable(var, file_groups)
    assert resolved == group1_1

def test__resolve_str_variable_unknown_module():    
    group1 = Group('myfile.py', 'FILE', 'File')
    node1_1 = Node('node1_1', None, None, group1, import_tokens=["node1_1"])
    group1.add_node(node1_1)
    file_groups = [group1]

    var = Variable("var1", "node1_2")

    resolved = _resolve_str_variable(var, file_groups)
    assert resolved == OWNER_CONST.UNKNOWN_MODULE

def test__wrap_as_variables():
    node1 = Node('node1_1', None, None, parent=None, line_number=10)
    node2 = Node('node1_2', None, None, parent=None, line_number=20)
    var_list = _wrap_as_variables([node1, node2])
    assert var_list == [
        Variable('node1_1', node1, line_number=node1.line_number), 
        Variable('node1_2', node2, line_number=node2.line_number)
    ]
    