import uvicorn
from tutor_agent.api import app

if __name__ == "__main__":
    uvicorn.run(
        "tutor_agent.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 


# python -m tutor_agent.server