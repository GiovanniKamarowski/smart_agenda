# Guia de Configuração - Frontend Smart Agenda

Este guia fornece instruções passo a passo para configurar e executar o frontend do Smart Agenda.

## Passo 1: Instalar Node.js e npm

Se você ainda não tem Node.js instalado, baixe em: https://nodejs.org/

As versões LTS são recomendadas. A instalação do Node.js inclui automaticamente o npm.

Para verificar se está instalado:
```bash
node --version
npm --version
```

## Passo 2: Instalar Dependências do Frontend

```bash
# Navegue para a pasta frontend
cd frontend

# Instale as dependências listadas em package.json
npm install
```

Este comando vai criar uma pasta `node_modules/` com todas as bibliotecas necessárias.

## Passo 3: Configurar Variáveis de Ambiente

Crie um arquivo `.env.local` na pasta `frontend/`:

```bash
# frontend/.env.local
VITE_API_BASE_URL=http://localhost:8000
```

Este arquivo já está listado em `.env.example`.

## Passo 4: Iniciar o Backend (FastAPI)

Em outro terminal, inicie o servidor FastAPI:

```bash
# Volte para a pasta raiz do projeto
cd ..

# Ative o ambiente virtual (se ainda não estiver ativado)
# Windows:
.\venv\Scripts\Activate.ps1

# Inicie o servidor FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Você deve ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Passo 5: Iniciar o Frontend (Vite)

Em outro terminal, navigate para a pasta frontend e inicie o servidor:

```bash
cd frontend

# Inicie o servidor de desenvolvimento
npm run dev
```

Você deve ver:
```
VITE v5.2.0  ready in 123 ms

➜  Local:   http://localhost:5173/
```

Acesse http://localhost:5173 no seu navegador.

## Passo 6: Testar a Conexão

1. Abra o frontend em http://localhost:5173
2. Tente criar um novo evento
3. Envie o formulário
4. Se funcionar, você verá a mensagem "Evento criado com sucesso!"

## Troubleshooting

### Erro: "Cannot GET /"
- Certifique-se de que o Vite está rodando em http://localhost:5173
- Verifique se não há outro aplicativo usando a porta 5173

### Erro: "Failed to fetch"
- Certifique-se de que o FastAPI está rodando em http://localhost:8000
- Verifique se CORS está configurado em `app/main.py`
- Abra o Console do Navegador (F12) e procure por erros CORS

### Erro: "npm: O termo 'npm' não é reconhecido"
- Node.js não está instalado ou não está no PATH
- Reinstale Node.js e reinicie o terminal
- Verifique com `npm --version`

### Erro: "Port 5173 already in use"
- Outro aplicativo está usando a porta 5173
- Use `-p 3000` para usar uma porta diferente: `npm run dev -- -p 3000`

## Estrutura do Projeto Frontend

```
frontend/
├── src/
│   ├── components/
│   │   ├── EventForm.tsx     - Formulário para criar/editar eventos
│   │   ├── EventList.tsx     - Lista de todos os eventos
│   │   └── EventCard.tsx     - Card individual de evento
│   ├── services/
│   │   └── api.ts            - Chamadas à API do backend
│   ├── App.tsx               - Componente raiz
│   ├── main.tsx              - Ponto de entrada
│   └── index.css             - Estilos globais com Tailwind
├── public/                   - Arquivos estáticos
├── index.html                - HTML principal
├── package.json              - Dependências npm
├── vite.config.ts            - Configuração do Vite
├── tsconfig.json             - Configuração do TypeScript
├── tailwind.config.js        - Configuração do Tailwind
└── postcss.config.js         - Configuração do PostCSS
```

## Recursos Úteis

- **Documentação React**: https://react.dev
- **Documentação Vite**: https://vitejs.dev
- **Documentação Tailwind**: https://tailwindcss.com/docs
- **Documentação React Hook Form**: https://react-hook-form.com
- **Documentação React Query**: https://tanstack.com/query/latest

## Desenvolvimento

Para adicionar novos componentes:

1. Crie o arquivo em `src/components/`
2. Use TypeScript para segurança de tipos
3. Adicione comentários explicando o funcionamento
4. Importe e use no `App.tsx`

Para adicionar novas chamadas à API:

1. Adicione a função em `src/services/api.ts`
2. Sempre retorne um tipo TypeScript (interface)
3. Use em componentes com `useQuery` ou `useMutation` do React Query

## Build para Produção

```bash
# Compila TypeScript e minifica o código
npm run build

# Visualiza o build localmente
npm run preview
```

Os arquivos compilados estarão em `dist/`.
