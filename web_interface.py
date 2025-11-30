"""
Web Interface for Fantasy Chatbot
FastAPI-based web server with real-time chat interface
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import asyncio
from typing import List, Dict, Optional
import logging
from datetime import datetime

from fantasy_chatbot import FantasyChatbot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global chatbot instance
chatbot = None
active_connections: List[WebSocket] = []

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove broken connections
                if connection in self.active_connections:
                    self.active_connections.remove(connection)

manager = ConnectionManager()

app = FastAPI(title="Persistent Fantasy Chatbot", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="web_static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page."""
    try:
        with open("web_static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse("""
        <html>
        <head><title>Fantasy Chatbot</title></head>
        <body>
            <h1>Fantasy Chatbot</h1>
            <p>Web interface files not found. Please run from the project directory.</p>
        </body>
        </html>
        """)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    global chatbot
    stats = {}
    if chatbot:
        stats = {
            "status": "healthy",
            "session_id": chatbot.session_id,
            "memory_stats": chatbot.get_memory_stats(),
            "memory_usage": chatbot.get_memory_usage()
        }
    else:
        stats = {"status": "not_initialized"}
    
    return stats

@app.post("/chat")
async def chat_endpoint(request: Dict):
    """HTTP endpoint for chat (alternative to WebSocket)."""
    global chatbot
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")
    
    user_input = request.get("message", "")
    if not user_input:
        raise HTTPException(status_code=400, detail="Message is required")
    
    try:
        result = chatbot.chat(user_input)
        return result
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memories")
async def get_memories(memory_type: Optional[str] = None, limit: int = 50):
    """Get stored memories."""
    global chatbot
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")
    
    if memory_type:
        memories = chatbot.memory_system.get_memories_by_type(memory_type, limit)
    else:
        # Get all types
        all_memories = []
        for mem_type in ["character", "location", "item", "event", "world"]:
            memories = chatbot.memory_system.get_memories_by_type(mem_type, limit//5)
            all_memories.extend(memories)
        memories = sorted(all_memories, key=lambda x: x['importance'], reverse=True)[:limit]
    
    return {"memories": memories}

@app.get("/world-state")
async def get_world_state():
    """Get current world state."""
    global chatbot
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")
    
    return {"world_state": chatbot.memory_system.get_world_state()}

@app.post("/search-memories")
async def search_memories(request: Dict):
    """Search memories by query."""
    global chatbot
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")
    
    query = request.get("query", "")
    memory_type = request.get("type")
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    results = chatbot.search_memories(query, memory_type)
    return {"results": results}

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time chat."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message_data = json.loads(data)
                user_input = message_data.get("message", "")
                
                if not user_input:
                    await manager.send_personal_message(
                        json.dumps({"error": "Message is required"}), 
                        websocket
                    )
                    continue
                
                # Process chat
                global chatbot
                result = chatbot.chat(user_input)
                
                # Send response back
                response_data = {
                    "type": "chat_response",
                    "user_input": user_input,
                    "response": result["response"],
                    "processing_time": result["processing_time"],
                    "memories_used": result["memories_used"],
                    "timestamp": datetime.now().isoformat()
                }
                
                await manager.send_personal_message(json.dumps(response_data), websocket)
                
                # Also broadcast to other connected clients for shared sessions
                broadcast_data = {
                    "type": "broadcast",
                    "session_id": chatbot.session_id,
                    "message": f"Someone said: {user_input[:50]}...",
                    "timestamp": datetime.now().isoformat()
                }
                await manager.broadcast(json.dumps(broadcast_data))
                
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    json.dumps({"error": "Invalid JSON"}), 
                    websocket
                )
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                await manager.send_personal_message(
                    json.dumps({"error": str(e)}), 
                    websocket
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/initialize")
async def initialize_chatbot(request: Dict = None):
    """Initialize the chatbot (can be called once at startup)."""
    global chatbot
    
    if chatbot is not None:
        return {"status": "already_initialized", "session_id": chatbot.session_id}
    
    try:
        # Initialize chatbot with request parameters
        session_id = request.get("session_id") if request else None
        model_name = request.get("model") if request else None
        use_quantization = request.get("use_quantization", True) if request else True
        
        chatbot = FantasyChatbot(
            session_id=session_id,
            model_name=model_name,
            use_quantization=use_quantization
        )
        
        # Load model in background
        asyncio.create_task(load_model_async())
        
        return {
            "status": "initializing",
            "session_id": chatbot.session_id,
            "message": "Model loading in background..."
        }
        
    except Exception as e:
        logger.error(f"Initialization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def load_model_async():
    """Load the LLM model asynchronously."""
    global chatbot
    try:
        logger.info("Loading LLM model in background...")
        chatbot.llm.load_model(quantization_4bit=chatbot.use_quantization)
        logger.info("LLM model loaded successfully!")
    except Exception as e:
        logger.error(f"Model loading failed: {e}")

def start_web_server(host: str = "127.0.0.1", port: int = 8000, 
                    auto_initialize: bool = True, **chatbot_kwargs):
    """
    Start the web server.
    
    Args:
        host: Host to bind to
        port: Port to bind to
        auto_initialize: Whether to automatically initialize chatbot
        **chatbot_kwargs: Additional arguments for chatbot initialization
    """
    global chatbot
    
    # Auto-initialize chatbot if requested
    if auto_initialize and chatbot is None:
        logger.info("Auto-initializing chatbot...")
        chatbot = FantasyChatbot(**chatbot_kwargs)
        
        # Load model synchronously for web server
        logger.info("Loading LLM model...")
        chatbot.llm.load_model(quantization_4bit=chatbot.use_quantization)
        logger.info("LLM model loaded!")
    
    logger.info(f"Starting web server on http://{host}:{port}")
    logger.info("Press Ctrl+C to stop the server")
    
    uvicorn.run(app, host=host, port=port, log_level="info")

if __name__ == "__main__":
    # Example usage
    start_web_server()