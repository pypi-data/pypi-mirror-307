from typing import Optional

from tree_sitter import Language, Parser, Node

from ._binding import language  # noqa: F401
from .nodes import Variable, Expression, Quantity, Unit

CAQTUS_LANGUAGE = Language(language())

parser = Parser(CAQTUS_LANGUAGE)


def parse(code: str) -> Expression:
    tree = parser.parse(bytes(code, "utf-8"))

    root_node = tree.root_node
    assert root_node.type == "expression"
    assert root_node.text

    if root_node.has_error:
        error_node = find_first_error(root_node)
        assert error_node is not None
        raise InvalidSyntaxError(
            f"Invalid syntax encountered while parsing expression <{code}>",
            (
                "",
                1,
                error_node.byte_range[0] + 1,
                root_node.text.decode("utf-8"),
                1,
                error_node.byte_range[1] + 1,
            ),
        )

    return build_expression(tree.root_node)


def find_first_error(node: Node) -> Node | None:
    if node.is_error or node.is_missing:
        return node

    for child in node.children:
        error = find_first_error(child)
        if error:
            return error


def build_expression(node: Node) -> Expression:
    assert node.type == "expression"
    assert len(node.children) == 1
    child = node.children[0]
    assert child.text

    match child:
        case Node(type="variable"):
            return build_variable(node.children[0])
        case Node(type="integer"):
            return int(child.text.decode("utf-8"))
        case Node(type="float"):
            return float(child.text.decode("utf-8"))
        case Node(type="quantity"):
            return build_quantity(node.children[0])
        case Node(type="call"):
            raise NotImplementedError("Call parsing is not implemented yet")
        case _:
            raise AssertionError(f"Unexpected node type: {node.type}")


def build_variable(node: Node) -> Variable:
    assert node.type == "variable"

    names = []

    # We skip the dots in the children list by jumping by 2
    for child in node.children:
        if child.type != ".":
            assert child.text
            names.append(child.text.decode("utf-8"))

    return Variable(tuple(names))


def build_quantity(node: Node) -> Quantity:
    assert node.type == "quantity"

    magnitude_node = node.child_by_field_name("magnitude")
    assert magnitude_node is not None
    assert magnitude_node.type == "float"
    assert magnitude_node.text
    magnitude = float(magnitude_node.text.decode("utf-8"))

    unit_node = node.child_by_field_name("units")
    assert unit_node is not None
    assert unit_node.type == "units"

    multiplicative_units = [
        build_unit_term(get_child_by_field_name(unit_node, "first"))
    ]

    for multiplicative_node in unit_node.children_by_field_name("multiplicative"):
        if multiplicative_node.type != "*":
            multiplicative_units.append(build_unit_term(multiplicative_node))

    divisional_units = [
        build_unit_term(divisional_node)
        for divisional_node in unit_node.children_by_field_name("divisive")
        if divisional_node.type != "/"
    ]

    return Quantity(magnitude, tuple(multiplicative_units), tuple(divisional_units))


def build_unit_term(node: Node) -> tuple[Unit, Optional[int]]:
    assert node.type == "unit_term"

    base_node = node.child_by_field_name("unit")
    assert base_node is not None
    assert base_node.type == "unit"
    assert base_node.text
    base = base_node.text.decode("utf-8")

    exponent_node = node.child_by_field_name("exponent")
    if exponent_node is None:
        return Unit(base), None
    else:
        assert exponent_node.type == "integer", exponent_node.type
        assert exponent_node.text
        exponent = int(exponent_node.text.decode("utf-8"))

        return Unit(base), exponent


def get_child_by_field_name(node: Node, field_name: str) -> Node:
    result = node.child_by_field_name(field_name)
    assert result is not None
    return result


class ParsingError(Exception):
    pass


class InvalidSyntaxError(ParsingError, SyntaxError):
    pass
