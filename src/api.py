import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx
import shutil
import uuid

app = FastAPI(
    title="Sistema de Triagem Médica",
    description="Frontend API que conecta ao MCP Server"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MCP_SERVER_URL = "http://localhost:8001"

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Envia uma mensagem para o MCP Server (Orquestrador).
    O MCP Server processa e retorna a resposta.
    """
    try:
        print(f"[API] Mensagem recebida: {request.message}")
        print(f"[API] Conectando ao MCP Server via SSE em {MCP_SERVER_URL}...")
        
        from mcp.client.sse import sse_client
        from mcp.client.session import ClientSession
        
        async with sse_client(f"{MCP_SERVER_URL}/sse", timeout=120.0) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                tools = await session.list_tools()
                print(f"[API] Ferramentas disponíveis: {tools}")
                
                result = await session.call_tool(
                    name="chat",
                    arguments={
                        "message": request.message,
                        "session_id": request.session_id
                    }
                )
                
                response_text = ""
                for content in result.content:
                    if hasattr(content, 'text'):
                        response_text += content.text
                    elif isinstance(content, str):
                        response_text += content
                
                if not response_text:
                    response_text = "Desculpe, não consegui processar sua solicitação."
                
                return ChatResponse(response=response_text, session_id=request.session_id)
        
    except Exception as e:
        import traceback
        print(f"[API] Erro: {str(e)}")
        print(traceback.format_exc())   
        raise HTTPException(status_code=500, detail=f"Erro de comunicação com MCP: {str(e)}")

@app.get("/health")
async def health():
    """Verifica status do servidor e do MCP."""
    try:
        async with httpx.AsyncClient() as client:
            mcp_health = await client.get(f"{MCP_SERVER_URL}/health", timeout=5.0)
            mcp_status = mcp_health.json()
    except:
        mcp_status = {"status": "offline"}
    
    return {
        "status": "ok",
        "server": "frontend-api",
        "mcp_server": mcp_status
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Recebe um arquivo de imagem, salva no servidor e retorna o caminho absoluto.
    Isso permite que os agentes leiam o arquivo como se fosse local.
    """
    try:
        upload_dir = Path(__file__).parent.parent / "data" / "uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_extension = Path(file.filename).suffix
        if not file_extension:
            file_extension = ".jpg" # Default fallback
            
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = upload_dir / unique_filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        print(f"[UPLOAD] Arquivo salvo em: {file_path}")
        
        return {
            "filename": file.filename,
            "filepath": str(file_path.absolute()),
            "message": "Upload realizado com sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha no upload: {str(e)}")

@app.get("/")
async def serve_chat():
    chat_path = Path(__file__).parent / "client" / "chat.html"
    return FileResponse(chat_path)