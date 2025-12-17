from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agente import AgenteAtendimento

app = FastAPI(title="Agente de Atendimento - Demo")

# Configurar CORS para permitir frontend acessar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instância do agente (em produção, seria por sessão/usuário)
agente = AgenteAtendimento()

class Mensagem(BaseModel):
    texto: str

class RespostaAgente(BaseModel):
    resposta: str
    sucesso: bool

@app.get("/")
def root():
    return {
        "mensagem": "API do Agente de Atendimento está rodando! 🤖",
        "endpoints": {
            "/chat": "POST - Enviar mensagem para o agente",
            "/resetar": "POST - Resetar conversa"
        }
    }

@app.post("/chat", response_model=RespostaAgente)
def chat(mensagem: Mensagem):
    """Endpoint principal para conversar com o agente"""
    try:
        resposta = agente.responder(mensagem.texto)
        return RespostaAgente(resposta=resposta, sucesso=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/resetar")
def resetar():
    """Reseta a conversa do agente"""
    agente.resetar_conversa()
    return {"mensagem": "Conversa resetada com sucesso! ✅"}

@app.get("/info")
def info_empresa():
    """Retorna informações da empresa"""
    from config import EMPRESA_NOME, EMPRESA_DESCRICAO, EMPRESA_PRODUTOS, EMPRESA_HORARIO
    return {
        "nome": EMPRESA_NOME,
        "descricao": EMPRESA_DESCRICAO,
        "produtos": EMPRESA_PRODUTOS,
        "horario": EMPRESA_HORARIO
    }
