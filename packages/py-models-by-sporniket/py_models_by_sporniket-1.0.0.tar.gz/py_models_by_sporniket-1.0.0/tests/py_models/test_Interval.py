# SPDX-License-Identifier: GPL-3.0-or-later
"""
---
(c) 2024 David SPORN
---
This is part of py-models -- A collection of basic data models in python.

py-models is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

py-models is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with py-models.
If not, see <https://www.gnu.org/licenses/>. 
---
"""

import pytest
from py_models import Interval


def test__Interval__has_expected_properties():
    # Legal instanciations
    a, b, c = Interval(length=0), Interval(1, length=5), Interval(1, end=6)
    assert a.start == 0
    assert a.length == 0
    assert a.end == 0
    assert len(a) == 0

    assert b.start == 1
    assert b.length == 5
    assert b.end == 6
    assert len(b) == 5

    assert c.start == 1
    assert c.length == 5
    assert c.end == 6
    assert len(c) == 5


def test__Interval__forbids_illegal_instanciations():
    # Each type of error
    with pytest.raises(ValueError) as error:
        Interval(-1, length=0)
    assert "invalid.must.be.positive.or.zero:start" in error.value.args
    assert len(error.value.args) == 1

    with pytest.raises(ValueError) as error:
        Interval(0, length=-1)
    assert "invalid.must.be.positive.or.zero:length" in error.value.args
    assert len(error.value.args) == 1

    with pytest.raises(ValueError) as error:
        Interval(0, end=-1)
    assert "invalid.too.low:end" in error.value.args
    assert len(error.value.args) == 1

    with pytest.raises(ValueError) as error:
        Interval(0)
    assert "invoke.missing.second.argument" in error.value.args
    assert len(error.value.args) == 1

    with pytest.raises(ValueError) as error:
        Interval(0, length=0, end=0)
    assert "invoke.too.much.argument" in error.value.args
    assert len(error.value.args) == 1

    # Will report all the errors
    with pytest.raises(ValueError) as error:
        Interval(-1)
    assert "invalid.must.be.positive.or.zero:start" in error.value.args
    assert "invoke.missing.second.argument" in error.value.args
    assert len(error.value.args) == 2

    with pytest.raises(ValueError) as error:
        Interval(-1, length=-1)
    assert "invalid.must.be.positive.or.zero:start" in error.value.args
    assert "invalid.must.be.positive.or.zero:length" in error.value.args
    assert len(error.value.args) == 2

    with pytest.raises(ValueError) as error:
        Interval(-1, length=-1, end=-2)
    assert "invalid.must.be.positive.or.zero:start" in error.value.args
    assert "invalid.must.be.positive.or.zero:length" in error.value.args
    assert "invoke.too.much.argument" in error.value.args
    assert "invalid.too.low:end" in error.value.args
    assert len(error.value.args) == 4


def test__Interval_isEmpty__works_as_expected():
    (a, b) = (Interval(0, length=0), Interval(0, length=1))
    assert a.isEmpty()
    assert not b.isEmpty()


def test__Interval_isBefore__is_an_ordering_relation():
    (a, b, c) = (Interval(9, length=0), Interval(10, length=0), Interval(11, length=0))
    # isBefore is transitive
    assert a.isBefore(b)
    assert b.isBefore(c)
    assert a.isBefore(c)
    # isBefore is anti symetrical
    assert not b.isBefore(a)
    # isBefore is reflexive
    assert b.isBefore(b)
    # is never before null
    assert not b.isBefore(None)


def test__Interval_isSmaller__is_an_ordering_relation():
    (a, b, c) = (Interval(0, length=9), Interval(0, length=10), Interval(0, length=11))
    # isSmaller is transitive
    assert a.isSmaller(b)
    assert b.isSmaller(c)
    assert a.isSmaller(c)
    # isSmaller is anti symetrical
    assert not b.isSmaller(a)
    # isSmaller is reflexive
    assert b.isSmaller(b)
    # is not smaller than None
    assert not b.isSmaller(None)


def test__Interval_isEndingBefore__is_an_ordering_relation():
    (a, b, c) = (
        Interval(9, length=10),
        Interval(10, length=10),
        Interval(11, length=10),
    )
    # isEndingBefore is transitive
    assert a.isEndingBefore(b)
    assert b.isEndingBefore(c)
    assert a.isEndingBefore(c)
    # isEndingBefore is anti symetrical
    assert not b.isEndingBefore(a)
    # isEndingBefore is reflexive
    assert b.isEndingBefore(b)
    # is not ending before None
    assert not b.isEndingBefore(None)


def test__Interval_isOutside__works_as_expected():
    a, b, c = Interval(5, length=10), Interval(15, length=10), Interval(3, length=15)
    assert a.isOutside(b)
    assert not a.isOutside(c)
    assert b.isOutside(a)
    assert not b.isOutside(c)
    assert not c.isOutside(a)
    assert not c.isOutside(b)


def test__Interval_isInside__is_an_ordering_relation():
    (a, b, c) = (Interval(9, length=2), Interval(8, length=4), Interval(7, length=6))
    # isInside is transitive
    assert a.isInside(b)
    assert b.isInside(c)
    assert a.isInside(c)
    # isInside is anti symetrical
    assert not b.isInside(a)
    # isInside is reflexive
    assert b.isInside(b)
    # is not inside None
    assert not b.isInside(None)
    # other things
    assert not a.isInside(Interval(7, length=2))
    assert not a.isInside(Interval(8, length=2))
    assert not a.isInside(Interval(10, length=2))
    assert not a.isInside(Interval(11, length=2))
