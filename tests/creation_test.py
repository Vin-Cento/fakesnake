from fakesnake.core import create_passwords


def test_passwords_num():
    passwords = create_passwords(5, 15, 25, "password")
    assert len(passwords) == 6


def test_passwords_error():
    try:
        create_passwords(1, 1, 1, "password")
        assert False
    except AssertionError:
        assert True
