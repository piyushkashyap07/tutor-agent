"""
Tutor Agent API

This module provides the REST API endpoints for the AI Tutor service. It handles chat interactions,
session management, and provides a health check endpoint.

API Endpoints:
    POST /api/chat
        Chat with the AI tutor agent. The agent can help with mathematics and physics topics.
        
        Request Body:
            {
                "message": "Can you help me with quadratic equations?",
                "session_id": "optional-session-id"  # Optional, for continuing conversations
            }
        
        Response:
            {
                "response": "Agent's response text",
                "session_id": "session-id-for-continuation"
            }

    GET /api/health
        Check the health status of the API service.
        
        Response:
            {
                "status": "healthy",
                "timestamp": "2024-03-21T10:30:00Z"
            }

Error Responses:
    400 Bad Request: Invalid input (e.g., empty message)
    500 Internal Server Error: Agent or server error
    503 Service Unavailable: Session management error
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from google.genai import types
from google.adk import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService

from tutor_agent.agent import root_agent

app = FastAPI(
    title="Tutor Agent API",
    description="""
    REST API for the AI Tutor service that provides personalized learning assistance.
    
    Features:
    - Interactive chat with an AI tutor
    - Support for mathematics and physics topics
    - Session management for continuous learning
    - Real-time responses with explanations
    
    The tutor can help with:
    - Mathematical concepts and calculations
    - Physics problems and formulas
    - Step-by-step explanations
    - Practice problems and solutions
    """,
    version="1.0.0",
    prefix="/api"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()

# Create API router
from fastapi import APIRouter
router = APIRouter(prefix="/api")

class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    
    Attributes:
        message (str): The user's question or message to the tutor
        session_id (Optional[str]): Optional session ID for continuing a conversation
    """
    message: str
    session_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "message": "Can you explain how to solve quadratic equations?",
                "session_id": "optional-session-id"
            }
        }

class ChatResponse(BaseModel):
    """
    Response model for chat endpoint.
    
    Attributes:
        response (str): The tutor's response to the user's message
        session_id (str): Session ID for continuing the conversation
    """
    response: str
    session_id: str

    class Config:
        schema_extra = {
            "example": {
                "response": "Let me explain quadratic equations step by step...",
                "session_id": "session-123"
            }
        }

class AgentError(Exception):
    """Base exception for agent-related errors."""
    pass

class SessionError(AgentError):
    """Exception for session-related errors."""
    pass

class ResponseError(AgentError):
    """Exception for response-related errors."""
    pass

async def run_agent(message: str, session_id: Optional[str] = None) -> tuple[str, str]:
    """Run the agent with the given message and return the response and session ID."""
    try:
        runner = Runner(
            app_name=root_agent.name,
            agent=root_agent,
            session_service=session_service,
            memory_service=memory_service
        )
        
        # Create or get session
        try:
            if session_id:
                session = await session_service.get_session(
                    app_name=root_agent.name,
                    user_id="api_user",
                    session_id=session_id
                )
                if not session:
                    session = await session_service.create_session(
                        app_name=root_agent.name,
                        user_id="api_user",
                        state={}
                    )
            else:
                session = await session_service.create_session(
                    app_name=root_agent.name,
                    user_id="api_user",
                    state={}
                )
        except Exception as e:
            raise SessionError(f"Failed to manage session: {str(e)}")
        
        # Create message content
        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=message)]
        )
        
        # Run agent
        last_event = None
        try:
            async for event in runner.run_async(
                user_id=session.user_id,
                session_id=session.id,
                new_message=content
            ):
                last_event = event
        except Exception as e:
            raise AgentError(f"Agent execution failed: {str(e)}")
        
        if not last_event or not last_event.content or not last_event.content.parts:
            raise ResponseError("No valid response from agent")
        
        response_text = "\n".join([p.text for p in last_event.content.parts if p.text])
        return response_text, session.id
        
    except SessionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Session error: {str(e)}"
        )
    except ResponseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Response error: {str(e)}"
        )
    except AgentError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

@router.post("/chat", 
    response_model=ChatResponse,
    summary="Chat with the AI tutor",
    description="""
    Send a message to the AI tutor and get a response.
    
    The tutor can help with:
    - Mathematics: Algebra, Calculus, Statistics, etc.
    - Physics: Mechanics, Thermodynamics, Electromagnetism, etc.
    
    You can continue a conversation by providing the session_id from a previous response.
    """,
    responses={
        200: {
            "description": "Successful response from the tutor",
            "content": {
                "application/json": {
                    "example": {
                        "response": "Let me help you understand this concept...",
                        "session_id": "session-123"
                    }
                }
            }
        },
        400: {
            "description": "Invalid request (e.g., empty message)",
            "content": {
                "application/json": {
                    "example": {"detail": "Message cannot be empty"}
                }
            }
        },
        500: {
            "description": "Server or agent error",
            "content": {
                "application/json": {
                    "example": {"detail": "Agent error: Failed to process request"}
                }
            }
        },
        503: {
            "description": "Service unavailable (e.g., session management error)",
            "content": {
                "application/json": {
                    "example": {"detail": "Session error: Failed to manage session"}
                }
            }
        }
    }
)
async def chat(request: ChatRequest):
    """
    Chat with the AI tutor agent.
    
    This endpoint allows users to:
    1. Ask questions about mathematics and physics
    2. Get step-by-step explanations
    3. Continue conversations using session_id
    4. Receive personalized learning assistance
    
    Args:
        request (ChatRequest): The chat request containing the user's message
            and optional session_id
    
    Returns:
        ChatResponse: The tutor's response and session information
    
    Raises:
        HTTPException: Various HTTP errors with descriptive messages
    """
    if not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )
    
    try:
        response_text, session_id = await run_agent(
            request.message,
            request.session_id
        )
        return ChatResponse(
            response=response_text,
            session_id=session_id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

@router.get("/health",
    summary="Check API health",
    description="Verify that the API service is running and healthy",
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "timestamp": "2024-03-21T10:30:00Z"
                    }
                }
            }
        }
    }
)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status and current timestamp
    """
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Include the router in the app
app.include_router(router)
