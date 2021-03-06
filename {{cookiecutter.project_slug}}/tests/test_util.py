# -*- coding: utf-8 -*-
"""Test utility functions."""

from {{ cookiecutter.project_slug }}.util import LazyObject, random_string
import pytest


def test_lazy():
    class FooDict(dict):
        # Support setattr on a dict
        pass

    d = FooDict({'a': 1})

    def init_object():
        d['a'] += 1
        return d

    obj = LazyObject(init_object)

    assert not obj.instantiated
    assert '<LazyObject wrapping <function' in repr(obj)
    assert d['a'] == 1

    # Object is instantiated here
    assert obj['a'] == 2
    assert obj.instantiated
    assert repr(obj) == "{'a': 2}"
    assert len(obj) == 1

    obj.abc = 'def'
    assert hasattr(obj, 'abc')
    assert obj.abc == 'def'
    assert d.abc == 'def'

    del obj.abc
    assert not hasattr(obj, 'abc')
    assert not hasattr(d, 'abc')

    obj['b'] = 3
    assert obj['b'] == 3
    assert d['b'] == 3
    assert 'b' in obj

    assert set(iter(obj)) == set(['a', 'b'])

    del obj['b']
    assert 'b' not in obj

    # Make sure we only ran init_object once
    assert d['a'] == 2

    obj.clear()
    assert len(obj) == 0
    assert len(d) == 0


def test_random_string():
    for n in (-2, -1):
        with pytest.raises(ValueError) as exc:
            random_string(n)
        assert 'Negative lengths are not allowed' in str(exc)

    for n in (1, 1.5, 3, 39):
        with pytest.raises(ValueError) as exc:
            random_string(n)
        assert 'The length must be a multiple of 4' in str(exc)

    for n in (0, 4, 8, 40):
        assert isinstance(random_string(n), type(u''))
        assert len(random_string(n)) == n
