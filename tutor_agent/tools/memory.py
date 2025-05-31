"""
Memory Tool

A specialized tool for maintaining learning progress and session history.
This tool helps create personalized learning experiences by tracking
student progress, concepts covered, and session context.

Features:
    - Session Management: Track learning sessions and their context
    - Progress Tracking: Monitor concepts covered and mastery levels
    - Personalized Learning: Adapt content based on student history
    - Concept Mapping: Build connections between related topics
    - Performance Analytics: Track improvement over time

Usage:
    The memory system is automatically used by the tutor agents to:
    - Maintain session context
    - Track learning progress
    - Provide personalized recommendations
    - Build on previous knowledge
    - Identify areas needing review

Example Use Cases:
    - Continuing a previous session
    - Reviewing previously covered topics
    - Tracking concept mastery
    - Identifying learning gaps
    - Providing personalized practice
"""

from datetime import datetime
import json
import os
from typing import Dict, Any

from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext
from google.adk.agents import Agent
from tutor_agent.profile import TUTOR_PROFILE

# Constants for state management
SYSTEM_TIME = "_time"
SESSION_INITIALIZED = "_session_initialized"
SESSION_KEY = "session"
PROFILE_KEY = "user_profile"
SESSION_START_TIME = "session_start_time"
SESSION_END_TIME = "session_end_time"
START_TIME = "start_time"
END_TIME = "end_time"

SAMPLE_SCENARIO_PATH = os.getenv(
    "TUTOR_AGENT_SCENARIO", "tutor_agent/profiles/tutor_default.json"
)

# Initialize the memory agent
memory_agent = Agent(
    model="gemini-2.0-flash",
    name="memory_agent",
    description="""
    A specialized memory agent that maintains learning progress and
    session history for personalized tutoring.
    
    The agent manages:
    - Learning session context
    - Concept mastery tracking
    - Student progress history
    - Personalized recommendations
    - Learning path optimization
    
    This helps create a continuous and adaptive
    learning experience for each student.
    """,
    instruction=f"""
    You are a memory agent that maintains learning progress and session history.
    Use the following profile to guide your interactions:
    
    {TUTOR_PROFILE}
    
    Always consider the student's learning history and progress
    when providing assistance or recommendations.
    """,
)

def memorize_list(key: str, value: str, tool_context: ToolContext):
    """
    Memorize pieces of information.

    Args:
        key: the label indexing the memory to store the value.
        value: the information to be stored.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    mem_dict = tool_context.state
    if key not in mem_dict:
        mem_dict[key] = []
    if value not in mem_dict[key]:
        mem_dict[key].append(value)
    return {"status": f'Stored "{key}": "{value}"'}


def memorize(key: str, value: str, tool_context: ToolContext):
    """
    Memorize pieces of information, one key-value pair at a time.

    Args:
        key: the label indexing the memory to store the value.
        value: the information to be stored.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    mem_dict = tool_context.state
    mem_dict[key] = value
    return {"status": f'Stored "{key}": "{value}"'}


def forget(key: str, value: str, tool_context: ToolContext):
    """
    Forget pieces of information.

    Args:
        key: the label indexing the memory to store the value.
        value: the information to be removed.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    if tool_context.state[key] is None:
        tool_context.state[key] = []
    if value in tool_context.state[key]:
        tool_context.state[key].remove(value)
    return {"status": f'Removed "{key}": "{value}"'}


def _set_initial_states(source: Dict[str, Any], target: State | dict[str, Any]):
    """
    Setting the initial session state given a JSON object of states.

    Args:
        source: A JSON object of states.
        target: The session state object to insert into.
    """
    if SYSTEM_TIME not in target:
        target[SYSTEM_TIME] = str(datetime.now())

    if SESSION_INITIALIZED not in target:
        target[SESSION_INITIALIZED] = True
        target.update(source)

        session = source.get(SESSION_KEY, {})
        if session:
            target[SESSION_START_TIME] = session[START_TIME]
            target[SESSION_END_TIME] = session[END_TIME]
            target[SESSION_START_TIME] = session[START_TIME]


def _load_precreated_itinerary(callback_context: CallbackContext):
    """
    Sets up the initial state.
    Set this as a callback as before_agent_call of the root_agent.
    This gets called before the system instruction is contructed.

    Args:
        callback_context: The callback context.
    """    
    data = {}
    with open(SAMPLE_SCENARIO_PATH, "r") as file:
        data = json.load(file)
        print(f"\nLoading Initial State: {data}\n")

    _set_initial_states(data["state"], callback_context.state)
