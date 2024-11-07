import sys

import sympy

sys.set_int_max_str_digits(10**8)


def calculator(expr: str) -> float | str:
    """
    What does this function do: Evaluates a mathematical expression and returns the result or an error message.

    When to use this function: Don't calculate any math problems by yourself, you are not good at math,
    you must use this function to calculate **all** the math calculations, this is the rule you must follow seriously.

    Args:
        expr (str): A string representing the mathematical expression to be evaluated (Which only contains const numbers).
        The expression can be simplified and should not contain commas or underscores.

    Returns:
        float | str: The result of the evaluated expression as a float, or an error message as a string.

    Examples:
        calculator('2.2+7*10') => 72.2
    """
    expr = expr.replace(',', '')
    expr = expr.replace('_', '')
    try:
        try:
            return sympy.simplify(expr, rational=None)
        except ValueError as ve:
            return ve.__repr__()
    except sympy.SympifyError as se:
        return se.__repr__()
