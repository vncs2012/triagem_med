from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="hermes3:8b", env="OLLAMA_MODEL")
    groq_api_key: str = Field(default="", env="GROQ_API_KEY")

    database_url: str = Field(
        default=f"sqlite:///{PROJECT_ROOT}/data/database.db",
        env="DATABASE_URL"
    )
    
    model_path: Path = Field(
        default=PROJECT_ROOT / "models" / "pneumonia_model.keras",
        env="MODEL_PATH"
    )
    
    mcp_server_host: str = Field(default="localhost", env="MCP_SERVER_HOST")
    mcp_server_port: int = Field(default=8765, env="MCP_SERVER_PORT")
    
    smtp_host: str = Field(default="smtp.example.com", env="SMTP_HOST")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_user: str = Field(default="", env="SMTP_USER")
    smtp_password: str = Field(default="", env="SMTP_PASSWORD")
    
    data_dir: Path = PROJECT_ROOT / "data"
    reports_dir: Path = PROJECT_ROOT / "data" / "reports"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ensure_directories()

    def _ensure_directories(self):
        directories = [
            self.data_dir,
            self.reports_dir,
            self.data_dir / "imgs",
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def is_model_available(self) -> bool:
        return self.model_path.exists()
    
    def get_database_path(self) -> Path:
        if self.database_url.startswith("sqlite:///"):
            return Path(self.database_url.replace("sqlite:///", ""))
        return self.data_dir / "database.db"
    
settings = Settings()

CLASSIFICATION_LABELS = {
    0: "NORMAL",
    1: "PNEUMONIA"
}

PRIORITY_LEVELS = {
    "BAIXO": 1,
    "MÉDIO": 2,
    "ALTO": 3,
    "CRÍTICO": 4
}

if __name__ == "__main__":
    print("=" * 50)
    print("CONFIGURAÇÕES DO SISTEMA")
    print("=" * 50)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Database URL: {settings.database_url}")
    print(f"Model Path: {settings.model_path}")
    print(f"Model Available: {settings.is_model_available()}")
    print(f"MCP Server: {settings.mcp_server_host}:{settings.mcp_server_port}")
    print(f"Ollama URL: {settings.ollama_base_url}")
    print(f"Ollama Model: {settings.ollama_model}")
    print("=" * 50)
