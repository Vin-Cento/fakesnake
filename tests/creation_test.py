from fakesnake.creation import *


def test_passwords_num():
    passwords = create_passwords(5, 15, 25)
    assert len(passwords) == 5


def test_passwords_error():
    try:
        create_passwords(1, 1, 1)
        assert False
    except AssertionError:
        assert True
