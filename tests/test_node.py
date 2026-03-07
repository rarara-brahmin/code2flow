import os
import pytest

from code2flow.model import Call, Variable, Node, Group

def test_uid(monkeypatch):
    # os.urandom を固定値に差し替える
    monkeypatch.setattr(os, "urandom", lambda n: b"\x01\x02\x03\x04")

    node = Node('my_node', None, None, None)
    assert node.uid == "node_01020304"

def test_repr():
    node = Node('my_node', None, None, "parent")
    r = repr(node)
    assert '<Node token=my_node' in r
    assert 'parent=parent' in r

def test_lt():
    group1 = Group('a_group', 'FILE', 'File')
    group2 = Group('b_group', 'FILE', 'File')
    node1 = Node('a_node', None, None, group1)
    node2 = Node('b_node', None, None, group2)
    assert (node1 < node2) is True
    assert (node2 < node1) is False

def test_first_group_not_instance():
    group = Group('myfile.py', 'FILE', 'File')
    node_p = Node('parent_node', None, None, group)
    node = Node('my_node', None, None, node_p)
    assert node.first_group() == group

def test_file_group():
    group = Group('myfile.py', 'FILE', 'File')
    node = Node('my_node', None, None, group)
    node2 = Node('child_node', None, None, node)
    assert node2.file_group() == group

def test_is_attr():
    group = Group('myfile.py', 'CLASS', 'Class')
    node = Node('my_node', None, None, group)
    assert node.is_attr() is True

def test_is_not_attr():
    node = Node('my_function', None, None, None)
    assert node.is_attr() is False

def test_token_with_ownership():
    group = Group('my_class', 'CLASS', 'Class')
    node = Node('my_node', None, None, group)
    assert node.token_with_ownership() == 'my_class.my_node'

def test_namespace_ownership():
    group1 = Group('my_class1', 'CLASS', 'Class')
    group2 = Group('my_class2', 'CLASS', 'Class', parent=group1)
    node = Node('my_node', None, None, group2)
    assert node.namespace_ownership() == 'my_class1.my_class2'

def test_label_line_number_implicit_constructor():
    node = Node(
        'my_node', 
        None, 
        None, 
        None, 
        line_number=42, 
        implicit_constructor=True)
    assert node.label() == '42: my_node (implicit constructor)'

def test_label_no_line_number_missing():
    node = Node(
        'my_node', 
        None, 
        None, 
        None, 
        line_number=None,
        missing=True)
    assert node.label() == 'my_node() (NotFound)'


def test_label_no_line_number():
    node = Node(
        'my_node', 
        None, 
        None, 
        None, 
        line_number=None)
    assert node.label() == 'my_node()'


def test_remove_from_parent():
    group = Group('myfile.py', 'FILE', 'File')
    node_test = Node('test_node', None, None, group)
    node1 = Node('node1', None, None, group)
    node2 = Node('node2', None, None, group)
    group.add_node(node_test)
    group.add_node(node1)
    group.add_node(node2)
    node_list = [node1, node2]
    node_test.remove_from_parent()
    assert node_test.first_group().nodes == node_list


def test_get_variables_no_line_num():
    var1 = Variable('var1', 'module.name')
    var2 = Variable('var2', 'another.module')
    node = Node('func', calls=[], variables=[var1, var2], parent=None)
    assert node.get_variables() == [var1, var2]

def test_get_variables_line_num():
    var1 = Variable('var1', 'module.name', line_number=1)
    var2 = Variable('var2', 'another.module', line_number=2)
    var3 = Variable('var3', 'third.module', line_number=3)
    node = Node('func', calls=[], variables=[var1, var2, var3], parent=None)
    assert node.get_variables(line_number=2) == [var2, var1]


def test_get_variables_line_num():
    var1 = Variable('var1', 'module.name', line_number=1)
    var2 = Variable('var2', 'another.module', line_number=2)
    var3 = Variable('var3', 'third.module', line_number=3)
    node = Node('func', calls=[], variables=[var1, var2, var3], parent=None)
    assert node.get_variables(line_number=2) == [var2, var1]


def test_get_variables_parents():
    var1_1 = Variable('var1', 'module.name', line_number=11)
    var1_2 = Variable('var2', 'another.module', line_number=12)
    var1_3 = Variable('var3', 'third.module', line_number=13)
    node1 = Node(
        'func1', 
        calls=[], 
        variables=[var1_1, var1_2, var1_3], 
        parent=None)
    
    var2_1 = Variable('var4', 'fourth.module', line_number=21)
    var2_2 = Variable('var5', 'fifth.module', line_number=22)
    var2_3 = Variable('var6', 'sixth.module', line_number=23)
    node2 = Node(
        'func2', 
        calls=[], 
        variables=[var2_1, var2_2, var2_3], 
        parent=node1)

    var3_1 = Variable('var7', 'seventh.module', line_number=31)
    var3_2 = Variable('var8', 'eighth.module', line_number=32)
    var3_3 = Variable('var9', 'ninth.module', line_number=33)
    node3 = Node(
        'func3', 
        calls=[], 
        variables=[var3_1, var3_2, var3_3], 
        parent=node2)
    
    var4_1 = Variable('var10', 'tenth.module', line_number=41)
    var4_2 = Variable('var11', 'eleventh.module', line_number=42)
    var4_3 = Variable('var12', 'twelfth.module', line_number=43)
    node4 = Node(
        'func4', 
        calls=[],
        variables=[var4_1, var4_2, var4_3],
        parent=node3)
    
    assert node4.get_variables() == [
        var4_3, var4_2, var4_1,
        var3_3, var3_2, var3_1,
        var2_3, var2_2, var2_1,
        var1_3, var1_2, var1_1
    ]