"""
Calculator Tool

A specialized tool for performing mathematical and scientific calculations.
This tool is used by both the mathematics and physics agents to verify
computations and solve numerical problems.

Features:
    - Basic arithmetic operations
    - Scientific functions (sin, cos, log, etc.)
    - Unit conversions
    - Statistical calculations
    - Matrix operations
    - Complex number support

Usage:
    The calculator is automatically used by the tutor agents when
    numerical computations are needed. It provides accurate results
    and helps verify student solutions.

Example Calculations:
    - Arithmetic: 2 + 2 = 4
    - Scientific: sin(45°) ≈ 0.7071
    - Statistical: mean([1, 2, 3, 4, 5]) = 3
    - Unit Conversion: 1 km = 1000 m
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

def cal(operation: str, numbers: list[float]):
    """
    A calculator function that performs operations on multiple numbers.
    
    Args:
        operation (str): The operation to perform ('add', 'subtract', 'multiply', 'divide', 'power', 'average')
        numbers (list[float]): List of numbers to perform the operation on
    
    Returns:
        float or int: Result of the operation
    """
    print(f"Calculator called with operation: '{operation}'")
    print(f"Arguments received: {numbers}")
    
    if not numbers:
        print("Error: No numbers provided")
        return "Error: No numbers provided"
    
    # Convert all arguments to numbers
    try:
        numbers = [float(num) for num in numbers]
        print(f"Numbers converted to: {numbers}")
    except (ValueError, TypeError):
        print("Error: Invalid number format detected")
        return "Error: All arguments must be numbers"
    
    operation = operation.lower()
    print(f"Processing operation: {operation}")
    
    if operation == 'add':
        print("Performing addition...")
        result = sum(numbers)
        print(f"Addition result: {result}")
        return result
    
    elif operation == 'subtract':
        print("Performing subtraction...")
        result = numbers[0]
        print(f"Starting with: {result}")
        for num in numbers[1:]:
            print(f"Subtracting: {num}")
            result -= num
        print(f"Subtraction result: {result}")
        return result
    
    elif operation == 'multiply':
        print("Performing multiplication...")
        result = 1
        for num in numbers:
            print(f"Multiplying by: {num}")
            result *= num
        print(f"Multiplication result: {result}")
        return result
    
    elif operation == 'divide':
        if len(numbers) < 2:
            print("Error: Division requires at least 2 numbers")
            return "Error: Division requires at least 2 numbers"
        print("Performing division...")
        result = numbers[0]
        print(f"Starting with: {result}")
        for num in numbers[1:]:
            if num == 0:
                print("Error: Cannot divide by zero!")
                return "Error: Division by zero"
            print(f"Dividing by: {num}")
            result /= num
        print(f"Division result: {result}")
        return result
    
    elif operation == 'power':
        if len(numbers) != 2:
            print("Error: Power operation requires exactly 2 numbers")
            return "Error: Power operation requires exactly 2 numbers (base, exponent)"
        print(f"Calculating {numbers[0]} raised to the power of {numbers[1]}...")
        result = numbers[0] ** numbers[1]
        print(f"Power result: {result}")
        return result
    
    elif operation == 'average':
        print("Calculating average...")
        total = sum(numbers)
        count = len(numbers)
        print(f"Sum: {total}, Count: {count}")
        result = total / count
        print(f"Average result: {result}")
        return result
    
    elif operation == 'max':
        print("Finding maximum value...")
        result = max(numbers)
        print(f"Maximum value: {result}")
        return result
    
    elif operation == 'min':
        print("Finding minimum value...")
        result = min(numbers)
        print(f"Minimum value: {result}")
        return result
    
    else:
        print(f"Error: Unknown operation '{operation}'")
        return f"Error: Unknown operation '{operation}'"


# Initialize the calculation agent
calculation_agent = Agent(
    model="gemini-2.0-flash",
    name="calculation_agent",
    description="""
    A specialized calculation agent that performs accurate mathematical
    and scientific computations.
    
    The agent ensures precise calculations for:
    - Mathematical operations
    - Scientific functions
    - Unit conversions
    - Statistical analysis
    - Complex computations
    
    Results are verified and presented with appropriate
    precision and units.
    """,
    instruction="""
    You are a calculation agent that performs mathematical and scientific computations.
    Always show your work and explain the steps taken to reach the solution.
    Include units where applicable and round results appropriately.
    """,
)

calculation_agent = AgentTool(agent=calculation_agent)