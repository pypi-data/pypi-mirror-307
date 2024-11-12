from __future__ import annotations

import attrs

type Number = int | float
type Scalar = Number | Quantity
type BinaryOperator = Add | Subtract | Multiply | Divide | Power
type UnaryOperator = Plus | Minus
type Expression = Variable | Scalar | Call | BinaryOperator | UnaryOperator


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

    @property
    def name(self) -> str:
        return ".".join(self.names)


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


@attrs.frozen
class Add:
    """Represents an addition operation in an expression.

    Attributes:
        left: The left operand.
        right: The right operand.
    """

    left: Expression
    right: Expression


@attrs.frozen
class Subtract:
    """Represents a subtraction operation in an expression.

    Attributes:
        left: The left operand.
        right: The right operand.
    """

    left: Expression
    right: Expression


@attrs.frozen
class Multiply:
    """Represents a multiplication operation in an expression.

    Attributes:
        left: The left operand.
        right: The right operand.
    """

    left: Expression
    right: Expression


@attrs.frozen
class Divide:
    """Represents a division operation in an expression.

    Attributes:
        left: The left operand.
        right: The right operand.
    """

    left: Expression
    right: Expression


@attrs.frozen
class Power:
    """Represents a power operation in an expression.

    Attributes:
        left: The base.
        right: The exponent.
    """

    left: Expression
    right: Expression

    @property
    def base(self) -> Expression:
        """Alias for the left operand."""

        return self.left

    @property
    def exponent(self) -> Expression:
        """Alias for the right operand."""

        return self.right


@attrs.frozen
class Plus:
    """Represents a unary plus operation in an expression.

    Attributes:
        operand: The operand.
    """

    operand: Expression


@attrs.frozen
class Minus:
    """Represents a unary minus operation in an expression.

    Attributes:
        operand: The operand.
    """

    operand: Expression
