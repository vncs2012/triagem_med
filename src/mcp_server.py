import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import JSONResponse
import uvicorn

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from src.agents.orchestrator.agent import root_agent

mcp = FastMCP("triagem-orquestrador")

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name="triagem_medica",
    session_service=session_service
)


@mcp.tool()
async def chat(message: str, session_id: str = "default") -> str:
    try:
        print(f"[MCP] Mensagem: {message}")
        
        session = await session_service.get_session(
            app_name="triagem_medica",
            user_id="mcp_user",
            session_id=session_id
        )
        
        if session is None:
            session = await session_service.create_session(
                app_name="triagem_medica",
                user_id="mcp_user",
                session_id=session_id
            )
        
        from google.genai import types
        user_content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=message)]
        )
        
        final_response = ""
        async for event in runner.run_async(
            user_id="mcp_user",
            session_id=session_id,
            new_message=user_content
        ):
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            final_response += part.text
                elif isinstance(event.content, str):
                    final_response += event.content
        
        if not final_response:
            final_response = "Desculpe, não consegui processar sua solicitação."
        
        print(f"[MCP] Resposta: {final_response[:100]}...")
        return final_response
        
    except Exception as e:
        import traceback
        error_msg = f"Erro: {str(e)}"
        print(f"[MCP] {error_msg}")
        print(traceback.format_exc())
        return error_msg


async def health(request):
    return JSONResponse({"status": "ok", "server": "mcp-orchestrator"})


app = Starlette(
    debug=True,
    routes=[
        Route("/health", health),
        Mount("/", app=mcp.sse_app()),
    ],
)

if __name__ == "__main__":
    print("=" * 60)
    print("🏥 SERVIDOR MCP - ORQUESTRADOR DE TRIAGEM MÉDICA")
    print("=" * 60)
    print("Protocolo: MCP sobre HTTP (SSE)")
    print("Ferramenta única: 'chat' -> fala com o Orquestrador")
    print("")
    print("Endpoints:")
    print("  GET  /health    -> Status do servidor")
    print("  POST / -> Mensagens MCP")
    print("")
    print("URL: http://localhost:8001")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
