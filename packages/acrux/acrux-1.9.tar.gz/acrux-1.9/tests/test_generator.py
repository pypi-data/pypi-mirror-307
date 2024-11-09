from acrux.generator import pair_generator


def test_pair_generator():
    generator = pair_generator([1, 2, 3])
    pairs = list(generator)

    assert len(pairs) == 3
    assert pairs[0] == (1, 2)
    assert pairs[1] == (1, 3)
    assert pairs[2] == (2, 3)
