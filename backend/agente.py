import httpx
from config import *

class AgenteAtendimento:
    def __init__(self):
        self.historico = []
        self.contexto_empresa = self._montar_contexto()
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def _montar_contexto(self):
        produtos_listados = "\n".join([f"• {p}" for p in EMPRESA_PRODUTOS])

        return f"""
{AGENTE_PERSONALIDADE}

INFORMAÇÕES DA EMPRESA:
Nome: {EMPRESA_NOME}
Descrição: {EMPRESA_DESCRICAO}
Horário: {EMPRESA_HORARIO}
WhatsApp: {EMPRESA_WHATSAPP}
Instagram: {EMPRESA_INSTAGRAM}

PRODUTOS DISPONÍVEIS:
{produtos_listados}

INSTRUÇÕES:
- Responda perguntas sobre produtos.
- Ajude a escolher itens.
- Se perguntarem preço, invente um valor razoável.
- Se o cliente quiser comprar, solicite o nome e confirme o pedido.
"""

    def responder(self, mensagem_usuario):
        self.historico.append({
            "role": "user",
            "content": mensagem_usuario
        })

        mensagens = [
            {"role": "system", "content": self.contexto_empresa}
        ] + self.historico

        try:
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": mensagens,
                "temperature": 0.7,
                "max_tokens": 300
            }

            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )

                response.raise_for_status()
                data = response.json()
                texto = data["choices"][0]["message"]["content"]

            self.historico.append({
                "role": "assistant",
                "content": texto
            })

            return texto

        except httpx.HTTPStatusError as e:
            return f"Erro na API Groq: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Desculpe, tive um problema interno 😅 Erro: {str(e)}"

    def resetar_conversa(self):
        self.historico = []
