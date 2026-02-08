# Guia para Corrigir e Executar o Frontend

## Problema Identificado

O frontend teve **importações não utilizadas** que causavam erros de compilação devido à configuração `"noUnusedLocals": true` no TypeScript.

**Arquivos corrigidos:**
- `src/App.tsx` - Removida importação não utilizada de `useEffect`
- `src/components/EventForm.tsx` - Removidas importações não utilizadas de `useState`, `useEffect` e `Controller`
- `src/components/EventList.tsx` - Removida importação não utilizada de `React`
- `src/components/EventCard.tsx` - Removida importação não utilizada de `React`

Também foi criado o arquivo `.env.local` com a configuração correta.

## Pré-requisitos

Para rodar o frontend, você precisa ter **Node.js v18+** instalado.

### Verificar se tem Node.js instalado:

```powershell
node --version
npm --version
```

### Se não tiver Node.js:

1. Acesse https://nodejs.org/
2. Baixe a versão LTS (Long Term Support)
3. Execute o instalador
4. Reinicie o terminal PowerShell
5. Verifique novamente com os comandos acima

## Instalação do Frontend

Após ter Node.js instalado:

```powershell
# Entre na pasta do frontend
cd frontend

# Instale as dependências
npm install
```

## Iniciando o Backend e Frontend

### Terminal 1 - Backend FastAPI:

```powershell
# Ative o ambiente virtual Python
.\venv\Scripts\Activate.ps1

# Inicie o servidor FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Você deve ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 - Frontend React:

```powershell
# Entre na pasta frontend
cd frontend

# Inicie o servidor de desenvolvimento
npm run dev
```

Você deve ver:
```
VITE v5.2.0  ready in 123 ms
➜  Local:   http://localhost:5173/
```

## Acessar a Aplicação

Abra seu navegador em **http://localhost:5173**

## Testando

1. Preencha o formulário com:
   - Título: "Reunião de Teste"
   - Email: seu.email@example.com
   - Data/Hora: Escolha uma data futura
   - Adicione um ou mais lembretes

2. Clique em "Criar"

3. Você deve ver a mensagem "Evento criado com sucesso!"

4. O evento aparecerá na lista abaixo

## Possíveis Problemas

### Erro: "npm: O termo 'npm' não é reconhecido"
- Node.js não está instalado
- Siga as instruções de instalação acima
- Reinicie o terminal PowerShell

### Erro: "Failed to fetch" no navegador
- Certifique-se de que o backend está rodando na porta 8000
- Abra o Console do Navegador (F12) para ver detalhes do erro
- Verifique se CORS está ativado em `app/main.py`

### Erro: "Port 5173 already in use"
- Outro aplicativo está usando a porta 5173
- Use uma porta diferente com: `npm run dev -- -p 3000`

## Build para Produção

```powershell
cd frontend
npm run build
npm run preview
```

---

**Todas as correções foram aplicadas automaticamente e commiteadas no Git.**
