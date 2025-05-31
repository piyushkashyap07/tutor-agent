"""
Physics Tutor Agent

A specialized agent for physics concepts and problem-solving. This agent provides
detailed explanations and step-by-step solutions for various physics topics.

Teaching Approach:
    1. Conceptual Understanding First:
        - Explain fundamental principles
        - Provide real-world examples
        - Build intuitive understanding
        - Use analogies and visualizations
    
    2. Problem Solving (Only When Requested):
        - Step-by-step calculations
        - Formula applications
        - Numerical solutions
        - Unit conversions

Capabilities:
    - Mechanics: Motion, forces, energy, momentum
    - Thermodynamics: Heat, temperature, entropy
    - Electromagnetism: Electric fields, magnetic fields, circuits
    - Waves: Sound, light, wave phenomena
    - Modern Physics: Quantum mechanics, relativity
    - Optics: Light behavior, lenses, mirrors

Tools:
    - Calculator: For numerical computations (only when explicitly requested)
    - Memory: For tracking learning progress and concepts covered

Example Teaching Flow:
    1. Student: "What is Coulomb's Law?"
       Response: Conceptual explanation with examples
    2. Student: "Can you show me how to calculate the force?"
       Response: Step-by-step calculation with explanation
"""

from google.adk.agents import Agent
from tutor_agent.sub_agents.physics import prompt
from tutor_agent.tools.calculator import calculation_agent

# Initialize the physics tutor agent
physics_agent = Agent(
    model="gemini-2.0-flash",
    name="physics_agent",
    description="""
    A specialized physics agent that provides comprehensive tutoring in physics.
    
    Teaching Philosophy:
    - Prioritize conceptual understanding
    - Use real-world examples and analogies
    - Build intuitive knowledge
    - Perform calculations only when requested
    
    Features:
    - Conceptual explanations
    - Real-world applications
    - Interactive learning
    - Step-by-step problem solving (on request)
    - Laboratory experiments
    
    The agent will:
    1. First explain concepts clearly
    2. Use examples and analogies
    3. Only perform calculations when explicitly asked
    4. Always explain the reasoning behind calculations
    
    Note: The agent focuses on building understanding
    before diving into calculations.
    """,
    instruction=prompt.PHYSICS_AGENT_INSTR,
    tools=[calculation_agent],  # For physics calculations (only when requested)
)