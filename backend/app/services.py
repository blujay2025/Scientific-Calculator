import re
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
    factorial_notation,
)

TRANSFORMATIONS = (
    standard_transformations
    + (implicit_multiplication_application, convert_xor, factorial_notation)
)


def _normalize_expression(expression: str, angle_mode: str = "RAD") -> str:
    expr = (expression or "").strip()
    if not expr:
        raise ValueError("Expression is required.")

    expr = expr.replace("×", "*").replace("÷", "/")
    expr = expr.replace("π", "pi")
    expr = expr.replace("√", "sqrt")
    expr = expr.replace("Ans", "ans")

    # Map calculator log/ln semantics.
    expr = re.sub(r"\bln\(", "nlog(", expr)
    expr = re.sub(r"\blog\(", "log10(", expr)

    # Scientific notation via EXP button.
    expr = expr.replace("EXP", "E10")
    expr = re.sub(r"(\d+(?:\.\d+)?)E10", r"\1*10^", expr)

    if angle_mode.upper() == "DEG":
        expr = re.sub(r"\basin\(", "asin_deg(", expr)
        expr = re.sub(r"\bacos\(", "acos_deg(", expr)
        expr = re.sub(r"\batan\(", "atan_deg(", expr)
        expr = re.sub(r"\bsin\(", "sin_deg(", expr)
        expr = re.sub(r"\bcos\(", "cos_deg(", expr)
        expr = re.sub(r"\btan\(", "tan_deg(", expr)

    return expr


def evaluate_expression(expression: str, angle_mode: str = "RAD", ans: float | int = 0):
    normalized = _normalize_expression(expression, angle_mode)

    allowed_symbols = {
        "pi": sp.pi,
        "e": sp.E,
        "ans": sp.Float(ans),
        "sqrt": sp.sqrt,
        "nlog": sp.log,
        "log10": lambda x: sp.log(x, 10),
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
        "asin": sp.asin,
        "acos": sp.acos,
        "atan": sp.atan,
        "sin_deg": lambda x: sp.sin(sp.pi * x / 180),
        "cos_deg": lambda x: sp.cos(sp.pi * x / 180),
        "tan_deg": lambda x: sp.tan(sp.pi * x / 180),
        "asin_deg": lambda x: sp.asin(x) * 180 / sp.pi,
        "acos_deg": lambda x: sp.acos(x) * 180 / sp.pi,
        "atan_deg": lambda x: sp.atan(x) * 180 / sp.pi,
    }

    try:
        parsed = parse_expr(normalized, local_dict=allowed_symbols, transformations=TRANSFORMATIONS, evaluate=True)
        evaluated = sp.N(parsed, 15)
    except Exception as exc:
        raise ValueError(f"Invalid expression: {exc}") from exc

    if evaluated.has(sp.zoo, sp.oo, -sp.oo, sp.nan):
        raise ValueError("Expression could not be evaluated.")

    result = _format_result(evaluated)
    return {
        "normalized_expression": normalized,
        "result": result,
    }


def _format_result(value):
    numeric = complex(value.evalf())
    if abs(numeric.imag) < 1e-12:
        real = numeric.real
        if abs(real - round(real)) < 1e-12:
            return str(int(round(real)))
        return f"{real:.12g}"
    return f"{numeric.real:.12g} + {numeric.imag:.12g}i"
