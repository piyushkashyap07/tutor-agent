"""
AI Tutor Agent

This module implements the main tutor agent using Google's Agent Development Kit (ADK).
The tutor agent serves as an educational coordinator that focuses exclusively on
academic questions and delegates specialized tasks to subject-specific sub-agents.

Core Focus:
    - Educational questions and learning assistance only
    - Mathematics and Physics subject areas
    - Academic problem-solving and explanations
    - Learning progress tracking

Role:
    The agent acts as a coordinator that:
    1. Evaluates if questions are education-related
    2. Delegates to appropriate subject specialists:
        - Maths Agent: For mathematical concepts and calculations
        - Physics Agent: For physics problems and formulas
    3. Maintains learning context and progress

Note:
    The agent will only respond to education-related questions.
    Non-educational queries will be politely redirected to focus on learning topics.

Usage:
    The agent is designed to be used through the API endpoints:
    - POST /api/chat: For educational interactions
    - GET /api/health: To check agent availability

Example Educational Topics:
    - Mathematics: Algebra, Calculus, Statistics
    - Physics: Mechanics, Thermodynamics, Electromagnetism
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent

from tutor_agent import prompt
from tutor_agent.sub_agents.maths.agent import maths_agent
from tutor_agent.sub_agents.physics.agent import physics_agent

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY environment variable is not set. "
        "Please set it in your .env file to use the tutor agent."
    )

# Initialize the root tutor agent
root_agent = Agent(
    model="gemini-2.0-flash-001",
    name="tutor_agent",
    description="""
    An educational AI tutor that focuses exclusively on academic learning assistance.
    
    Primary Responsibilities:
    - Handle education-related questions only
    - Coordinate with specialized subject agents
    - Maintain learning context and progress
    - Ensure focused academic interactions
    
    Subject Areas:
    - Mathematics (via Maths Agent)
        - Algebra, Calculus, Statistics
        - Problem-solving and calculations
    - Physics (via Physics Agent)
        - Mechanics, Thermodynamics
        - Scientific concepts and formulas
    
    The agent will:
    - Evaluate if questions are education-related
    - Delegate to appropriate subject specialists
    - Maintain learning progress
    - Focus solely on academic assistance
    
    Note: The agent will politely redirect non-educational
    queries to focus on learning topics.
    """,
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        maths_agent,  # Specialized agent for mathematical concepts
        physics_agent  # Specialized agent for physics problems
    ]
)
