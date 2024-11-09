import typing as tp


def pair_generator(array: tp.List) -> tp.Generator:
    """
    Pair generator.
    Example:
        array = ['a', 'b', 'c', 'd', 'e']
        list(pair_generator(array, 2)) -> [a, b], [a, c], [a, d], [b, c], [b, d], [c, d]
    :param array:
    """
    n = len(array)
    for i in range(n):
        for j in range(i + 1, n, 1):
            yield array[i], array[j]
