from __future__ import annotations

import attrs

type Number = int | float
type Scalar = Number | Quantity
type Expression = Variable | Scalar | Call


@attrs.frozen
class Variable:
    """Represents a variable in an expression.

    Attributes:
        names: The names of the variable.
            This can be a single name or a tuple of names which then represent the
            variable ``a.b.c`` as ``("a", "b", "c")``.

            It is guaranteed that the names are not empty.
    """

    names: tuple[str, ...]


@attrs.frozen
class Quantity:
    """Represents a quantity in an expression.

    Attributes:
        magnitude: The magnitude of the quantity.
        multiplicative_units: The units that are at the numerator of the quantity.
            Each unit is a tuple of the unit name and the exponent.
        divisional_units: The units that are at the denominator of the quantity.
            Each unit is a tuple of the unit name and the exponent.
    """

    magnitude: float
    multiplicative_units: tuple[UnitTerm, ...]
    divisional_units: tuple[UnitTerm, ...] = ()


@attrs.frozen
class UnitTerm:
    """Represents a unit term in a quantity.

    Attributes:
        unit: The base unit symbol.
        exponent: The exponent of the base unit.
            If this is ``None``, the exponent is 1.
    """

    unit: str
    exponent: int | None = None


@attrs.frozen
class Call:
    """Represents a function call in an expression.

    Attributes:
        function: The function name.
            It is guaranteed that this is not empty and to be a simple identifier.
            Dotted names are not allowed here.
        args: The positional arguments passed to the function.
    """

    function: str
    args: tuple[Expression, ...] = ()
