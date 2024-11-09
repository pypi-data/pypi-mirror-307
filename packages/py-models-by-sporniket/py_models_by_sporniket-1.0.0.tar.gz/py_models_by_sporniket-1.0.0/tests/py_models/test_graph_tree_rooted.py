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

from py_models import NodeRT


def test__NodeRT__has_expected_properties():
    olderSibling, youngerSibling, child1, child2 = (
        NodeRT(),
        NodeRT(),
        NodeRT(),
        NodeRT(),
    )
    a = NodeRT(
        children=[child1, child2],
    )
    parent = NodeRT(children=[olderSibling, a, youngerSibling])

    assert a.parent is parent
    assert a.previous is olderSibling
    assert a.next is youngerSibling
    assert len(a.children) == 2
    assert a.children[0] == child1
    assert a.children[1] == child2

    # side effects -- referenced nodes are relinked according to specified relations.
    assert a in parent.children
    assert a is olderSibling.next
    assert a is youngerSibling.previous
    assert a is child1.parent
    assert a is child2.parent
    assert child2 is child1.next
    assert child1 is child2.previous
    assert parent is olderSibling.parent
    assert parent is youngerSibling.parent
    assert olderSibling in parent.children
    assert youngerSibling in parent.children

    # Predicates
    assert not a.isRoot()
    assert parent.isRoot()
    assert not a.isLeaf()
    assert child1.isLeaf()
    assert not a.isFirstChild()
    assert not a.isLastChild()
    assert child1.isFirstChild()
    assert not child1.isLastChild()
    assert not child2.isFirstChild()
    assert child2.isLastChild()
    assert olderSibling.isFirstChild()
    assert not olderSibling.isLastChild()
    assert not youngerSibling.isFirstChild()
    assert youngerSibling.isLastChild()


def test__NodeRT__rejects_list_of_children_with_duplicates():
    child = NodeRT()

    with pytest.raises(ValueError) as error:
        NodeRT(children=[child, child])
    assert "child.already.in.list" == error.value.args[0]
    assert 1 == error.value.args[1]
    assert len(error.value.args) == 2

    with pytest.raises(ValueError) as error:
        NodeRT().adopt([child, child])
    assert "child.already.in.list" == error.value.args[0]
    assert 1 == error.value.args[1]
    assert len(error.value.args) == 2


def test__NodeRT__rejects_list_of_children_that_contains_ancestors():
    grandParent = NodeRT()
    parent = NodeRT(parent=grandParent)

    with pytest.raises(ValueError) as error:
        NodeRT(parent=parent, children=[parent])
    assert "child.is.ancestor" == error.value.args[0]
    assert 0 == error.value.args[1]
    assert len(error.value.args) == 2

    with pytest.raises(ValueError) as error:
        NodeRT(parent=parent, children=[grandParent])
    assert "child.is.ancestor" == error.value.args[0]
    assert 0 == error.value.args[1]
    assert len(error.value.args) == 2

    with pytest.raises(ValueError) as error:
        NodeRT(parent=parent).adopt([parent])
    assert "child.is.ancestor" == error.value.args[0]
    assert 0 == error.value.args[1]
    assert len(error.value.args) == 2

    with pytest.raises(ValueError) as error:
        NodeRT(parent=parent).adopt([grandParent])
    assert "child.is.ancestor" == error.value.args[0]
    assert 0 == error.value.args[1]
    assert len(error.value.args) == 2


def test__NodeRT_isAncestorOf__is_a_strict_ordering_relation():
    a = NodeRT()
    b = NodeRT(parent=a)
    c = NodeRT(parent=b)

    assert a.isAncestorOf(b)
    assert b.isAncestorOf(c)
    # Anti-Reflexive
    assert not a.isAncestorOf(a)
    assert not b.isAncestorOf(b)
    assert not c.isAncestorOf(c)
    # Anti-symetric
    assert not b.isAncestorOf(a)
    # Transitive
    assert a.isAncestorOf(c)


def test__NodeRT_isDescendantOf__is_a_strict_ordering_relation():
    a = NodeRT()
    b = NodeRT(parent=a)
    c = NodeRT(parent=b)

    assert c.isDescendantOf(b)
    assert b.isDescendantOf(a)
    # Anti-Reflexive
    assert not a.isDescendantOf(a)
    assert not b.isDescendantOf(b)
    assert not c.isDescendantOf(c)
    # Anti-symetric
    assert not a.isDescendantOf(b)
    # Transitive
    assert c.isDescendantOf(a)


def test__NodeRT_isOlderSiblingOf__is_a_strict_ordering_relation():
    a, b, c = NodeRT(), NodeRT(), NodeRT()
    NodeRT(children=[c, b, a])

    assert c.isOlderSiblingOf(b)
    assert b.isOlderSiblingOf(a)
    # Anti-Reflexive
    assert not a.isOlderSiblingOf(a)
    assert not b.isOlderSiblingOf(b)
    assert not c.isOlderSiblingOf(c)
    # Anti-symetric
    assert not a.isOlderSiblingOf(b)
    # Transitive
    assert c.isOlderSiblingOf(a)


def test__NodeRT_isYoungerSiblingOf__is_a_strict_ordering_relation():
    a, b, c = NodeRT(), NodeRT(), NodeRT()
    NodeRT(children=[a, b, c])

    assert c.isYoungerSiblingOf(b)
    assert b.isYoungerSiblingOf(a)
    # Anti-Reflexive
    assert not a.isYoungerSiblingOf(a)
    assert not b.isYoungerSiblingOf(b)
    assert not c.isYoungerSiblingOf(c)
    # Anti-symetric
    assert not a.isYoungerSiblingOf(b)
    # Transitive
    assert c.isYoungerSiblingOf(a)
