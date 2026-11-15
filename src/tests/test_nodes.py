import cmath

import pytest

from src.core.exceptions import (
    IncompleteExpressionError,
    InvalidOperationError,
    UnboundVariableError,
)
from src.core.nodes import (
    BinaryNode,
    EmptySlot,
    NumberNode,
    UnaryNode,
    VariableNode,
)

"""
Module created to test the functionality
of Base Classes of Nodes for the
calculator.
"""


def test_number_is_complete() -> None:
    """
    Test created to evaluate if a NumberNode
    is complete.
    """

    number_node = NumberNode(5)
    assert number_node.is_complete == True


def test_number_evaluate() -> None:
    """
    Test created to evaluate if the
    evaluation of a NumberNode is
    correct.
    """

    number_node = NumberNode(5)
    assert number_node.evaluate == 5


def test_number_LaTeX_is_right() -> None:
    """
    Test created to evaluate if a
    NumberNode's LaTeX representation
    is right.
    """

    number_node = NumberNode(5)
    assert number_node.to_latex == "5"


def test_number_node_constant_pi_LaTeX_is_correct() -> None:
    """
    Test created to evaluate if a NumberNode with
    pi as a constant's LaTeX representation is right
    or not.
    """

    number_node = NumberNode("pi")
    assert number_node.to_latex == r"\pi"


def test_number_node_constant_e_LaTeX_is_correct() -> None:
    """
    Test created to evaluate if a NumberNode with
    e as a constant's LaTeX representation is right
    or not.
    """

    number_node = NumberNode("e")
    assert number_node.to_latex == r"e"


def test_number_node_constant_phi_LaTeX_is_correct() -> None:
    """
    Test created to evaluate if a NumberNode with
    phi as a constant's LaTeX representation is right
    or not.
    """

    number_node = NumberNode("phi")
    assert number_node.to_latex == r"\phi"


def test_number_node_constant_i_LaTeX_is_correct() -> None:
    """
    Test created to evaluate if a NumberNode with
    i as a constant's LaTeX representation is right
    or not.
    """

    number_node = NumberNode("i")
    assert number_node.to_latex == r"i"


def test_number_node_constant_pi_evaluates_well() -> None:
    """
    Test created to evaluate if a NumberNode with
    pi as a constant evaluates to the correct numeric
    value or not.
    """

    number_node = NumberNode("pi")
    assert number_node.evaluate == cmath.pi


def test_number_node_constant_e_evaluates_well() -> None:
    """
    Test created to evaluate if a NumberNode with
    e as a constant evaluates to the correct numeric
    value or not.
    """

    number_node = NumberNode("e")
    assert number_node.evaluate == cmath.e


def test_number_node_constant_phi_evaluates_well() -> None:
    """
    Test created to evaluate if a NumberNode with
    phi as a constant evaluates to the correct numeric
    value or not.
    """

    number_node = NumberNode("phi")
    assert number_node.evaluate == (1 + cmath.sqrt(5)) / 2


def test_number_node_constant_i_evaluates_well() -> None:
    """
    Test created to evaluate if a NumberNode with
    i as a constant evaluates to the correct numeric
    value or not.
    """

    number_node = NumberNode("i")
    assert number_node.evaluate == 1j


def test_empty_slot_is_complete() -> None:
    """
    Test created to evaluate if a EmptySlot
    object is not complete.
    """

    empty_slot = EmptySlot()
    assert empty_slot.is_complete == False


def test_empty_slot_LaTeX_is_right() -> None:
    """
    Test created to evaluate if a
    EmptySlot's LaTeX representation
    is right.
    """

    empty_slot = EmptySlot()
    assert empty_slot.to_latex == r"\square"


def test_empty_slot_evaluate() -> None:
    """
    Test created to evaluate if the
    evaluation of a EmptySlot raises
    an IncompleteExpressionError.
    """

    empty_slot = EmptySlot()
    with pytest.raises(IncompleteExpressionError):
        _ = empty_slot.evaluate


def test_binary_node_only_left() -> None:
    """
    Test created to evaluate if a BinaryNode created
    with only a left node correctly assigns an EmptySlot
    to the right branch and is incomplete.
    """
    node = BinaryNode(NumberNode(2), None, "+")
    assert isinstance(node.right, EmptySlot)
    assert node.is_complete == False


def test_binary_node_only_right() -> None:
    """
    Test created to evaluate if a BinaryNode created
    with only a right node correctly assigns an EmptySlot
    to the left branch and is incomplete.
    """
    node = BinaryNode(None, NumberNode(3), "+")
    assert isinstance(node.left, EmptySlot)
    assert node.is_complete == False


def test_binary_node_none_both() -> None:
    """
    Test created to evaluate if a BinaryNode created
    with no arguments correctly assigns EmptySlots
    to both branches and is incomplete.
    """
    node = BinaryNode(None, None, "+")
    assert isinstance(node.left, EmptySlot)
    assert isinstance(node.right, EmptySlot)
    assert node.is_complete == False


def test_binary_node_invalid_operator_latex() -> None:
    """
    Test created to evaluate if a BinaryNode with an
    invalid operator raises an InvalidOperationError
    when trying to get its LaTeX representation.
    """
    node = BinaryNode(NumberNode(2), NumberNode(3), "operador_falso")
    with pytest.raises(InvalidOperationError):
        _ = node.to_latex


def test_binary_node_invalid_operator_evaluate() -> None:
    """
    Test created to evaluate if a BinaryNode with an
    invalid operator raises an InvalidOperationError
    when trying to evaluate it.
    """
    node = BinaryNode(NumberNode(2), NumberNode(3), "operador_falso")
    with pytest.raises(InvalidOperationError):
        _ = node.evaluate


def test_binary_node_sum_is_complete() -> None:
    """
    Test created to evaluate if a BinaryNode
    for a sum is complete or not.
    """

    binary_node_for_proof = BinaryNode(NumberNode(5), NumberNode(2), "+")
    assert binary_node_for_proof.is_complete == True


def test_binary_node_product_evaluates_well() -> None:
    """
    Test created to evaluate if a BinaryNode
    for a product evaluates well.
    """

    binary_node_for_proof = BinaryNode(NumberNode(5), NumberNode(2), "*")
    assert binary_node_for_proof.evaluate == 10


def test_binary_node_sum_LaTeX_is_correct() -> None:
    """
    Test created to evaluate if a BinaryNode's
    LaTeX representation for a sum is correct
    or not.
    """

    binary_node_for_proof = BinaryNode(NumberNode(5), NumberNode(2), "+")
    assert binary_node_for_proof.to_latex == "(5 + 2)"


def test_anidation_in_binary_node_is_complete() -> None:
    """
    Test created to evaluate if a BinaryNode
    anidated is read as complete or not.
    """

    binary_node_one_for_proof = BinaryNode(NumberNode(3), NumberNode(4), "*")
    binary_node_two_for_proof = BinaryNode(
        NumberNode(3), binary_node_one_for_proof, "+"
    )
    assert binary_node_two_for_proof.is_complete == True


def test_anidation_in_binary_node_evaluates_well() -> None:
    """
    Test created to evaluate if a BinaryNode
    anidated evaluates right or not.
    """

    binary_node_one_for_proof = BinaryNode(NumberNode(3), NumberNode(4), "*")
    binary_node_two_for_proof = BinaryNode(
        NumberNode(3), binary_node_one_for_proof, "+"
    )
    assert binary_node_two_for_proof.evaluate == 15


def test_anidation_in_binary_node_LaTeX_is_well() -> None:
    """
    Test created to evaluate if a BinaryNode
    anidated LaTeX's representation is right or not.
    """

    binary_node_one_for_proof = BinaryNode(NumberNode(3), NumberNode(4), "*")
    binary_node_two_for_proof = BinaryNode(
        NumberNode(3), binary_node_one_for_proof, "+"
    )
    assert binary_node_two_for_proof.to_latex == r"(3 + (3 \times 4))"


def test_unary_node_with_nones_is_incomplete() -> None:
    """
    Test created to evaluate if an UnaryNode
    whit a None in its argument is incomplete.
    """

    unary_node_for_proof = UnaryNode("sqrt", None)
    assert unary_node_for_proof.is_complete == False


def test_unary_node_is_complete() -> None:
    """
    Test created to evaluate if an UnaryNode
    is complete or not.
    """

    unary_node_for_proof = UnaryNode("sqrt", NumberNode(16))
    assert unary_node_for_proof.is_complete == True


def test_unary_node_evaluates_well() -> None:
    """
    Test created to evaluate if an UnaryNode
    evaluates correctly or not.
    """

    unary_node_for_proof = UnaryNode("sqrt", NumberNode(16))
    assert unary_node_for_proof.evaluate == 4


def test_unary_node_LaTeX_is_correct() -> None:
    """
    Test created to evaluate if an UnaryNode's
    LaTeX representation is correct or not.
    """

    unary_node_for_proof = UnaryNode("sqrt", NumberNode(16))
    assert unary_node_for_proof.to_latex == r"\sqrt{16}"


def test_unary_node_anidated_evaluates_well() -> None:
    """
    Test created to evaluate if an UnaryNode with an
    BinaryNode anidated evaluates well or not.
    """

    binary_node_for_proof = BinaryNode(NumberNode(2), NumberNode(3), "+")
    unary_node_for_proof = UnaryNode("sin", binary_node_for_proof)
    assert unary_node_for_proof.evaluate == cmath.sin(2 + 3)


def test_unary_node_anidated_LaTeX_is_correct() -> None:
    """
    Test created to evaluate if an UnaryNode with an
    BinaryNode anidated's LaTeX representation is
    correct or not.
    """

    binary_node_for_proof = BinaryNode(NumberNode(2), NumberNode(3), "+")
    unary_node_for_proof = UnaryNode("sin", binary_node_for_proof)
    assert unary_node_for_proof.to_latex == r"\sin((2 + 3))"


def test_unary_node_latex_cbrt() -> None:
    """
    Test created to evaluate if an UnaryNode representing
    a cube root correctly generates its LaTeX representation.
    """
    node = UnaryNode("cbrt", NumberNode(8))
    assert node.to_latex == r"\sqrt[3]{8}"


def test_unary_node_latex_abs() -> None:
    """
    Test created to evaluate if an UnaryNode representing
    an absolute value correctly generates its LaTeX representation.
    """
    node = UnaryNode("abs", NumberNode(-5))
    assert node.to_latex == r"\left|-5\right|"


def test_unary_node_latex_floor() -> None:
    """
    Test created to evaluate if an UnaryNode representing
    a floor function correctly generates its LaTeX representation.
    """
    node = UnaryNode("floor", NumberNode(5.5))
    assert node.to_latex == r"\lfloor 5.5 \rfloor"


def test_unary_node_latex_ceil() -> None:
    """
    Test created to evaluate if an UnaryNode representing
    a ceil function correctly generates its LaTeX representation.
    """
    node = UnaryNode("ceil", NumberNode(5.5))
    assert node.to_latex == r"\lceil 5.5 \rceil"


def test_unary_node_latex_factorial() -> None:
    """
    Test created to evaluate if an UnaryNode representing
    a factorial correctly generates its LaTeX representation.
    """
    node = UnaryNode("factorial", NumberNode(5))
    assert node.to_latex == "5!"


def test_unary_node_latex_neg() -> None:
    """
    Test created to evaluate if an UnaryNode representing
    a negation correctly generates its LaTeX representation.
    """
    node = UnaryNode("neg", NumberNode(5))
    assert node.to_latex == "-5"


def test_unary_node_latex_standard_function() -> None:
    """
    Test created to evaluate if an UnaryNode representing
    a standard function (like cosine) correctly generates
    its LaTeX representation with parentheses.
    """
    node = UnaryNode("cos", NumberNode(0))
    assert node.to_latex == r"\cos(0)"


def test_unary_node_invalid_operator_latex() -> None:
    """
    Test created to evaluate if an UnaryNode with an
    invalid operator raises an InvalidOperationError
    when trying to get its LaTeX representation.
    """
    node = UnaryNode("operador_falso", NumberNode(2))
    with pytest.raises(InvalidOperationError):
        _ = node.to_latex


def test_unary_node_invalid_operator_evaluate() -> None:
    """
    Test created to evaluate if an UnaryNode with an
    invalid operator raises an InvalidOperationError
    when trying to evaluate it.
    """
    node = UnaryNode("operador_falso", NumberNode(2))
    with pytest.raises(InvalidOperationError):
        _ = node.evaluate


def test_variable_node_is_complete() -> None:
    """
    Test created to evaluate if a VariableNode
    created correctly is complete or not.
    """

    variable_node = VariableNode("x")
    assert variable_node.is_complete == True


def test_variable_node_LaTeX_is_correct() -> None:
    """
    Test created to evaluate if a VariableNode's
    LaTeX representation is right or not.
    """

    variable_node = VariableNode("x")
    assert variable_node.to_latex == "x"


def test_variable_node_greek_LaTeX_is_correct() -> None:
    """
    Test created to evaluate if a VariableNode with
    a greek letter as a value's LaTeX representation
    is righ or not.
    """

    variable_node = VariableNode("alpha")
    assert variable_node.to_latex == r"\alpha"


def test_variable_node_greek_upper_LaTeX_is_correct() -> None:
    """
    Test created to evaluate if a VariableNode with
    an upper greek letter as a value's LaTeX
    representation is righ or not.
    """

    variable_node = VariableNode("Alpha")
    assert variable_node.to_latex == r"A"


def text_variable_node_evaluate_raises_an_error() -> None:
    """
    Test created to evaluate if the evaluate function
    of a VariableNode raises an UnboundVariableError
    or not.
    """

    variable_node = VariableNode("\alpha")
    with pytest.raises(UnboundVariableError):
        _ = variable_node.evaluate
