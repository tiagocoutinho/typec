# -*- coding: utf-8 -*-
#
# This file is part of the typec library
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT license. See LICENSE for more info.

import pytest

from typec import (Int, Float, Str, Bool, Number, PositiveInt, PositiveNumber,
                   Iterable, Module, Class, Callable, checked)

def test_types():
    assert Int.check(10) == 10
    with pytest.raises(TypeError):
        Int.check('hello')

def __test_iplus(iplus):
    assert iplus(10, 15) == 25
    with pytest.raises(TypeError):
        iplus('hello',15)
    with pytest.raises(TypeError):
        iplus(1.1, 15)

def test_f():
    def iplus(a, b):
        Int.check(a)
        Int.check(b)
        return a + b
    __test_iplus(iplus)

def test_f_annotated():
    @checked
    def iplus(a: Int, b: Int):
        return a + b
    __test_iplus(iplus)

def test_f_func():
    @checked
    def func(it : Iterable, mod: Module):
        return it, mod

    import time
    p1 = [1,2,3,4]
    assert func(p1, time) == (p1, time)
    with pytest.raises(TypeError):
        func(1.1, time)
    with pytest.raises(TypeError):
        func(p1, 'hello')


def test_class():
    @checked
    class Player:
        name: Str
        age: PositiveInt
        points: int
        position: Int

        def __init__(self, name, age, position):
            self.name = name
            self.age = age
            self.points = 0
            self.position = position

        def left(self, dpos):
            self.position -= dpos

        def right(self, dpos):
            self.position += dpos

    player = Player('Brian', 25, 1)
    assert player.position == 1
    player.left(10)
    assert player.position == -9
    player.points = 10
    assert player.points == 10

    with pytest.raises(TypeError):
        player.name = True
    with pytest.raises(ValueError):
        player.age = 0
    with pytest.raises(TypeError):
        player.position = 'hello'
    with pytest.raises(TypeError):
        player.points = 1.1
    with pytest.raises(TypeError):
        player.left(10.1)
    with pytest.raises(TypeError):
        Player(1, 25, 1)
    with pytest.raises(TypeError):
        Player('Brian', 25, 1.1)
