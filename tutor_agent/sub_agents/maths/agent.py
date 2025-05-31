"""
Mathematics Tutor Agent

A specialized agent for mathematical concepts and calculations. This agent provides
detailed explanations and step-by-step solutions for various mathematical topics.

Capabilities:
    - Basic Arithmetic: Addition, subtraction, multiplication, division
    - Algebra: Equations, inequalities, functions
    - Calculus: Derivatives, integrals, limits
    - Statistics: Probability, distributions, data analysis
    - Number Theory: Prime numbers, modular arithmetic
    - Geometry: Shapes, theorems, proofs

Tools:
    - Calculator: For numerical computations and verifications
    - Memory: For tracking learning progress and concepts covered

Example Topics:
    - Solving quadratic equations
    - Understanding derivatives
    - Statistical analysis
    - Geometric proofs
    - Matrix operations
"""

from google.adk.agents import Agent
from tutor_agent.sub_agents.maths import prompt
from tutor_agent.tools.calculator import calculation_agent

# Initialize the mathematics tutor agent
maths_agent = Agent(
    model="gemini-2.0-flash",
    name="maths_agent",
    description="""
    A specialized mathematical agent that provides comprehensive tutoring in mathematics.
    
    Features:
    - Step-by-step problem solving
    - Conceptual explanations
    - Practice problems
    - Real-world applications
    - Interactive learning
    
    The agent uses a calculator tool for computations and maintains
    learning progress through the memory system.
    """,
    instruction=prompt.MATHS_AGENT_INSTR,
    tools=[calculation_agent],  # For mathematical computations
)