# SPDX-License-Identifier: GPL-3.0-or-later
"""
An _interval_ between a and b, with `a <= b`, will mean all the numbers between a _included_ and b _excluded_,
i.e. in mathematical notation : `[a..b[`

* `a` is the `start` of the interval
* `b` is the `end` of the interval
* `b - a` is the length of the interval
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


class Interval:
    """Interval defined with integers."""

    ### TODO : work with numbers too --> given i an interval and j a number (int or float) :
    ### * i.isBefore(j) returns True if i.end <= j
    ### * i.isEndingBefore(j) returns True if i.end <= j
    ###
    ### * i.__contains__(j)
    ###   * j a number --> returns True if i.start <= j and j < i.end --> delegate
    ###   * j an interval --> returns j.isInside(i)

    def __init__(self, start: int = 0, *, length: int = None, end: int = None):
        """An interval is defined by its start value and either its end, or its length"""
        # sanity checks
        errors = []
        if start < 0:
            errors += ["invalid.must.be.positive.or.zero:start"]
        if length is not None:
            if end is not None:
                errors += ["invoke.too.much.argument"]
                self._checkEnd(start, end, errors)
            if length < 0:
                errors += ["invalid.must.be.positive.or.zero:length"]
        elif end is not None:
            self._checkEnd(start, end, errors)
        else:
            errors += ["invoke.missing.second.argument"]

        if len(errors) > 0:
            listBody = ",".join(errors)
            raise ValueError(*errors)

        # OK, proceed
        self._start = start
        self._length = length if length is not None else end - start
        self._end = end if end is not None else start + length

    def _checkEnd(self, start, end, errors):
        if end < start:
            errors += ["invalid.too.low:end"]

    @property
    def start(self) -> int:
        return self._start

    @property
    def length(self) -> int:
        return self._length

    @property
    def end(self) -> int:
        return self._end

    def __len__(self):
        return self.length

    # ========[ predicates ] ========
    def isEmpty(self) -> bool:
        return self._length == 0

    def isBefore(self, x: "Interval") -> bool:
        return (x is not None) and self._isBefore(x)

    def isEndingBefore(self, x: "Interval") -> bool:
        return (x is not None) and (self.start + self.length <= x.start + x.length)

    def isSmaller(self, x: "Interval") -> bool:
        return x is not None and self._isSmaller(x)

    def isOutside(self, x: "Interval") -> bool:
        return (x is None) or x._isBeginningAfter(self) or self._isBeginningAfter(x)

    def isInside(self, x: "Interval") -> bool:
        return (x is not None) and x._isBefore(self) and self._isEndingBefore(x)

    # ========[ predicates internal ] ========
    def _isBefore(self, x: "Interval") -> bool:
        return self.start <= x.start

    def _isEndingBefore(self, x: "Interval") -> bool:
        return self.start + self.length <= x.start + x.length

    def _isBeginningAfter(self, x: "Interval") -> bool:
        return self.start >= x.start + x.length

    def _isSmaller(self, x: "Interval") -> bool:
        return self.length <= x.length
