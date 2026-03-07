import pytest

from code2flow.model import Call, Variable, Node, Group

def test_call_repr_and_to_string():
    call = Call('my_function', owner_token='my_module', is_library=True)
    r = repr(call)
    assert '<Call owner_token=my_module' in r
    assert 'token=my_function' in r


def test_call_to_string_only_token():
    call = Call('my_function')
    assert call.to_string() == 'my_function()'


def test_call_to_string_with_owner():
    call = Call('my_function', owner_token='my_module')
    assert call.to_string() == 'my_module.my_function()'


def test_call_attr_with_owner():
    call = Call('my_function', owner_token='my_module')
    assert call.is_attr() is True


def test_call_attr_without_owner():
    call = Call('my_function')
    assert call.is_attr() is False


def test_call_matches_variable_obj_method():
    call = Call('my_method', owner_token='my_obj')
    nodes = [Node('my_method', calls=[], variables=[], parent=None)]

    class MockPointsTo:
        def __init__(self, nodes):
            self.nodes = nodes
    mockPointsTo = MockPointsTo(nodes)

    var = Variable('my_obj', points_to=mockPointsTo)
    assert call.matches_variable(var) == nodes[0]


def test_call_matches_variable_inherits_obj_method():
    call = Call('my_method', owner_token='my_obj')
    nodes = [Node('my_method', calls=[], variables=[], parent=None)]

    class MockPointsTo:
        def __init__(self, nodes):
            self.inherits = [nodes]
    mockPointsTo = MockPointsTo(nodes)

    var = Variable('my_obj', points_to=mockPointsTo)
    assert call.matches_variable(var) == nodes[0]


def test_call_matches_variable_no_match():
    unknown_var = "UNKNOWN_VAR"
    call = Call('my_method', owner_token='my_obj')
    var = Variable('my_obj', points_to=unknown_var)
    assert call.matches_variable(var) == unknown_var


def test_call_matches_variable_node():
    call = Call('my_method')
    node = Node('my_method', calls=[], variables=[], parent=None)
    var = Variable('my_method', points_to=node)
    assert call.matches_variable(var) == node

def test_call_matches_variable_group():
    call = Call('my_function', owner_token='my_class')
    group = Group('myfile.py', 'NAMESPACE', 'Namespace')
    var = Variable('my_function', points_to=group)
    assert call.matches_variable(var) == None

def test_call_matches_variable_group_2parts():
    call = Call('my_function', owner_token='my_lib.my_class')
    group = Group('myfile.py', 'NAMESPACE', 'Namespace')
    var = Variable('my_function', points_to=group)
    assert call.matches_variable(var) == None

def test_call_matches_variable_namespace_ownership():
    call = Call('my_function', owner_token='my_lib.my_class')
    parent=Group('my_class', group_type='CLASS', display_type='Class')
    var = Variable('my_class', points_to=parent)
    node = Node('my_function', calls=[call], variables=[var], parent=parent)
    group = Group('myfile.py', 'NAMESPACE', 'Namespace')
    group.add_node(node)
    var = Variable('my_lib', points_to=group)
    assert call.matches_variable(var) == node

def test_call_matches_self_attr():
    call = Call('my_function', owner_token='my_lib.my_class')
    var = Variable('my_lib', points_to=call)
    assert call.matches_variable(var) == None

def test_call_matches_self_attr():
    call = Call('my_function', owner_token='my_lib.my_class')
    var = Variable('my_lib', points_to=call)
    assert call.matches_variable(var) == None

def test_call_matches_constructor():
    call = Call('my_function')
    parent = Group('my_class', group_type='CLASS', display_type='Class')
    var = Variable('my_var1', points_to=parent)
    node = Node(
        'my_node', 
        calls=[call], 
        variables=[var], 
        parent=parent, 
        is_constructor=True)
    group = Group('myfile.py', 'CLASS', 'Class')
    group.add_node(node)
    var = Variable('my_function', points_to=group)
    assert call.matches_variable(var) == node

def test_call_no_match():
    call = Call('my_function1')
    group = Group('myfile.py', 'CLASS', 'Class')
    var = Variable('my_function2', points_to=group)
    assert call.matches_variable(var) == None
