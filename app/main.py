from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading

from app.interfaces.api.router import router
from app.infrastructure.db.database import Base, engine
from app.infrastructure.db import models
from app.infrastructure.scheduler.reminder_scheduler import ReminderScheduler

# Cria a instância principal da aplicação FastAPI
app = FastAPI(title="SmartAgenda API")

# Configura CORS (Cross-Origin Resource Sharing) para permitir requisições do frontend
# Permite que o frontend rodando em http://localhost:5173 faça requisições para a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Frontend em desenvolvimento
        "http://localhost:3000",  # Alternativa
        "http://127.0.0.1:5173",  # Localhost alternativo
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, PUT, DELETE, etc)
    allow_headers=["*"],  # Permite todos os headers
)

# Registra as rotas da aplicação
app.include_router(router)

# Instância do scheduler que roda em background verificando lembretes
scheduler = ReminderScheduler(intervalo_segundos=10)


@app.on_event("startup")
def startup_event():
    """
    Evento executado quando a aplicação inicia.

    Funções:
    - cria tabelas no banco automaticamente caso ainda não existam
    - inicia o scheduler em uma thread separada para não travar a API
    """

    # Garante que todas as tabelas (eventos, lembretes, notificacoes) existam
    Base.metadata.create_all(bind=engine)
    print("[MAIN] Tabelas verificadas/criadas com sucesso.")

    # Inicia scheduler em background
    thread = threading.Thread(target=scheduler.iniciar, daemon=True)
    thread.start()
    print("[MAIN] Scheduler iniciado com sucesso.")


@app.on_event("shutdown")
def shutdown_event():
    """
    Evento executado quando a aplicação encerra.

    Função:
    - para o scheduler de forma segura
    """

    scheduler.parar()
    print("[MAIN] Scheduler finalizado com sucesso.")
