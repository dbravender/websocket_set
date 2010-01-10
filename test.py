from setgame import is_set, Card

def test_is_set():
    assert is_set([Card(1, 'o', 'r', 'f'),
                   Card(2, 'd', 'r', 'f'),
                   Card(3, 's', 'r', 'f')])
