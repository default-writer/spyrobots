from src.app import add

def test_add():
    # assign
    a = 1
    b = 2
    # action
    c = add (a, b)
    # assert
    assert c == 3
