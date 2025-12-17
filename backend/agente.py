from groq import Groq
from config import *

client = Groq(api_key=GROQ_API_KEY)

class AgenteAtendimento:
    def __init__(self):
        self.historico = []
        self.contexto_empresa = self._montar_contexto()

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
            resposta = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=mensagens,
                temperature=0.7,
                max_tokens=300
            )

            texto = resposta.choices[0].message.content

            self.historico.append({
                "role": "assistant",
                "content": texto
            })

            return texto

        except Exception as e:
            return f"Desculpe, tive um problema interno 😅 Erro: {str(e)}"

    def resetar_conversa(self):
        self.historico = []
