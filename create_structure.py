import os

structure = [
    "smart_agenda/app/__init__.py",
    "smart_agenda/app/main.py",

    "smart_agenda/app/core/config.py",
    "smart_agenda/app/core/exceptions.py",

    "smart_agenda/app/domain/entities.py",
    "smart_agenda/app/domain/interfaces.py",
    "smart_agenda/app/domain/events.py",

    "smart_agenda/app/application/dtos.py",
    "smart_agenda/app/application/services/agenda_service.py",
    "smart_agenda/app/application/services/notification_service.py",

    "smart_agenda/app/infrastructure/db/database.py",
    "smart_agenda/app/infrastructure/db/models.py",
    "smart_agenda/app/infrastructure/db/repositories.py",

    "smart_agenda/app/infrastructure/notifications/email_adapter.py",
    "smart_agenda/app/infrastructure/notifications/whatsapp_adapter.py",

    "smart_agenda/app/interfaces/api/router.py",
    "smart_agenda/app/interfaces/api/dependencies.py",
    "smart_agenda/app/interfaces/api/v1/endpoints/eventos.py",

    "smart_agenda/app/interfaces/api/schemas/evento.py",
    "smart_agenda/app/interfaces/api/schemas/lembrete.py",

    "smart_agenda/alembic/versions/.gitkeep",

    "smart_agenda/tests/unit/.gitkeep",
    "smart_agenda/tests/integration/.gitkeep",

    "smart_agenda/.env",
    "smart_agenda/.gitignore",
    "smart_agenda/alembic.ini",
    "smart_agenda/requirements.txt",
    "smart_agenda/README.md",
]

for path in structure:
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            if path.endswith(".gitignore"):
                f.write(".env\n__pycache__/\n*.pyc\n.vscode/\n")
            elif path.endswith("README.md"):
                f.write("# Smart Agenda\n")
            elif path.endswith("requirements.txt"):
                f.write("fastapi\nuvicorn\nsqlalchemy\nalembic\npydantic\npython-dotenv\n")
            elif path.endswith(".env"):
                f.write("ENV=dev\n")
            elif path.endswith("__init__.py"):
                f.write("")
            elif path.endswith(".gitkeep"):
                f.write("")

print("Estrutura criada com sucesso!")
