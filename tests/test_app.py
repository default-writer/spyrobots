from src.app import add, sub, double

def test_add():
    # assign
    a = 1
    b = 2
    # action
    c = add(a, b)
    # assert
    assert c == 3

def test_sub():
    # assign
    a = 1
    b = 2
    # action
    c = sub(a, b)
    # assert
    assert c == -1

def test_double():
    # assign
    a = 1
    b = 2
    # action
    c = double(a, b)
    # assert
    assert c == 6
