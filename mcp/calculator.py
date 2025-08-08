from mcp.server.fastmcp import FastMCP

import math


# instant
mcp = FastMCP("This is a calculator")


# tools
@mcp.tool()
def add(a: float, b: float) -> float:
    """
    Add two numbers.
    """
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """
    Subtract two numbers.
    """
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers.
    """
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """
    Divide two numbers.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


@mcp.tool()
def power(base: float, exponent: float) -> float:
    """
    Raise a number to the power of another number.
    """
    return math.pow(base, exponent)


@mcp.tool()
def square_root(number: float) -> float:
    """
    Calculate the square root of a number.
    """
    if number < 0:
        raise ValueError("Cannot calculate square root of a negative number.")
    return math.sqrt(number)


@mcp.tool()
def factorial(number: int) -> int:
    """
    Calculate the factorial of a number.
    """
    if number < 0:
        raise ValueError("Cannot calculate factorial of a negative number.")
    if number == 0 or number == 1:
        return 1
    result = 1
    for i in range(2, number + 1):
        result *= i
    return result


@mcp.tool()
def logarithm(number: float, base: float = 10) -> float:
    """
    Calculate the logarithm of a number with a specified base.
    """
    if number <= 0:
        raise ValueError("Logarithm is undefined for non-positive numbers.")
    if base <= 1:
        raise ValueError("Base must be greater than 1.")
    return math.log(number, base)


@mcp.tool()
def absolute_value(number: float) -> float:
    """
    Calculate the absolute value of a number.
    """
    return abs(number)


# add a dynamic greeting resource
@mcp.resource("greeting//{name}")
def greeting(name: str) -> str:
    """
    Generate a greeting message for a given name.
    """
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run(transport="stdio")
