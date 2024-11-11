from typing import Optional, NewType

import attrs

type Number = int | float
type Scalar = Number | Quantity
type Expression = Variable | Scalar


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

Unit = NewType("Unit", str)

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
    multiplicative_units: tuple[tuple[Unit, Optional[int]], ...]
    divisional_units: tuple[tuple[Unit, Optional[int]], ...]
