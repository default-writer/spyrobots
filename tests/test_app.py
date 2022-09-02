from src.app import add, sub, double, say_hello

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

def test_say_hello():
    # assign
    # action
    c = say_hello()
    # assert
    assert c == "hello, world!"
