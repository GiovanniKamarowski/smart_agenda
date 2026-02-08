# Smart Agenda - Frontend

Frontend web moderno para o Smart Agenda, desenvolvido com React, TypeScript, Tailwind CSS e Vite.

## Tecnologias

- **React 18** - Biblioteca UI moderna
- **TypeScript** - Segurança de tipos em JavaScript
- **Vite** - Bundler rápido e moderno
- **Tailwind CSS** - Framework CSS com utilidades
- **React Hook Form** - Gerenciamento eficiente de formulários
- **React Query** - Caching e sincronização de estado do servidor
- **Axios** - Cliente HTTP para chamadas à API
- **DayJS** - Manipulação de datas (leve e moderna)

## Pré-requisitos

- Node.js 18+ 
- NPM ou Yarn

## Instalação

```bash
# Entre na pasta do frontend
cd frontend

# Instale as dependências
npm install
```

## Desenvolvimento

```bash
# Inicie o servidor de desenvolvimento
npm run dev
```

O servidor rodará em `http://localhost:5173`

### Configuração de CORS

O frontend se conecta à API em `http://localhost:8000` por padrão. 

**Importante**: O backend FastAPI precisa ter CORS habilitado para aceitar requisições do frontend.

No `app/main.py`, adicione:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Estrutura do Projeto

```
frontend/
├── src/
│   ├── components/          # Componentes React reutilizáveis
│   │   ├── EventForm.tsx    # Formulário de criar/editar eventos
│   │   ├── EventList.tsx    # Lista de eventos
│   │   └── EventCard.tsx    # Card individual de evento
│   ├── services/
│   │   └── api.ts           # Funções de chamadas à API
│   ├── App.tsx              # Componente raiz
│   ├── main.tsx             # Ponto de entrada React
│   └── index.css            # Estilos globais
├── public/                  # Arquivos estáticos
├── index.html               # Arquivo HTML principal
├── vite.config.ts           # Configuração do Vite
├── tsconfig.json            # Configuração do TypeScript
├── tailwind.config.js       # Configuração do Tailwind
├── postcss.config.js        # Configuração do PostCSS
└── package.json             # Dependências do projeto
```

## API Endpoints

O frontend consome os seguintes endpoints do backend:

### Listar Eventos
```
GET /eventos/
Retorna: Evento[]
```

### Criar Evento
```
POST /eventos/
Body:
{
  "titulo": "Reunião",
  "data_horario": "2026-02-08T14:00:00",
  "email_usuario": "user@example.com",
  "descricao": "Opcional",
  "lembretes": [{ "minutos_antecedencia": 15 }]
}
Retorna: Evento
```

### Atualizar Evento
```
PUT /eventos/{id}
Body: (mesmo formato do POST)
Retorna: Evento
```

### Deletar Evento
```
DELETE /eventos/{id}
Retorna: { "status": "ok", "mensagem": "Evento excluído." }
```

### Health Check
```
GET /health
Retorna: { "status": "ok" }
```

## Build para Produção

```bash
# Compila TypeScript e faz bundle do projeto
npm run build

# Visualiza o build localmente
npm run preview
```

## Funcionalidades

✅ **Criar Eventos** - Formulário completo com validação
✅ **Listar Eventos** - Exibição em cards com informações resumidas
✅ **Editar Eventos** - Modifica eventos existentes
✅ **Deletar Eventos** - Remove eventos com confirmação
✅ **Lembretes** - Adiciona múltiplos lembretes (minutos antes)
✅ **Cache Inteligente** - React Query mantém dados atualizados
✅ **Validação** - Campos obrigatórios e validação de email
✅ **Design Responsivo** - Interface que funciona em diferentes tamanhos

## Contribuindo

Para desenvolver novos features:

1. Crie uma branch: `git checkout -b feat/nova-funcionalidade`
2. Faça commit: `git commit -m 'feat: descrição da mudança'`
3. Abra um Pull Request

## Licença

MIT
