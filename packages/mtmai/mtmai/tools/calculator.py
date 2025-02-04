def calculator_tool(a: float, b: float, operator: str) -> str:
    try:
        if operator == "+":
            return str(a + b)
        elif operator == "-":
            return str(a - b)
        elif operator == "*":
            return str(a * b)
        elif operator == "/":
            if b == 0:
                return "Error: Division by zero"
            return str(a / b)
        else:
            return "Error: Invalid operator. Please use +, -, *, or /"
    except Exception as e:
        return f"Error: {str(e)}"
