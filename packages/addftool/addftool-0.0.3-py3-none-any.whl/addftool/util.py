def rangeexpand(txt):
    lst = []
    for r in txt.split(','):
        if '-' in r[1:]:
            r0, r1 = r[1:].split('-', 1)
            r1 = r1.strip()
            lst += range(int(r[0] + r0), int(r1) + 1)
        elif not r.strip():
            continue
        else:
            lst.append(int(r.strip()))
    return lst


def test_rangeexpand():
    import pytest

    assert rangeexpand('1, 3-5, 7') == [1, 3, 4, 5, 7]
    assert rangeexpand('1, 3-5, 7, 10-12') == [1, 3, 4, 5, 7, 10, 11, 12]
    assert rangeexpand('1-5') == [1, 2, 3, 4, 5]
    assert rangeexpand('1-5, 7-10') == [1, 2, 3, 4, 5, 7, 8, 9, 10]
    assert rangeexpand('') == []
    assert rangeexpand('1') == [1]
    assert rangeexpand('1-1') == [1]
    assert rangeexpand('1-1, 3-3, 5-5') == [1, 3, 5]
    assert rangeexpand('1-1, 3-3, 5-5, 7-7') == [1, 3, 5, 7]
    
    with pytest.raises(ValueError):
        rangeexpand('1-2-3')

    with pytest.raises(ValueError):
        rangeexpand('1 7-9')
