import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

EMPRESA_NOME = "Boutique Goods"
EMPRESA_DESCRICAO = "Loja online de produtos artesanais únicos e personalizados"
EMPRESA_PRODUTOS = [
    "Velas aromáticas artesanais",
    "Sabonetes naturais",
    "Decoração em macramê",
    "Cestas personalizadas",
    "Kits presente"
]
EMPRESA_HORARIO = "Segunda a Sexta: 9h às 18h | Sábado: 9h às 14h"
EMPRESA_WHATSAPP = "(11) 99999-9999"
EMPRESA_INSTAGRAM = "@boutique_goods"

AGENTE_PERSONALIDADE = f"""
Você é a atendente virtual da {EMPRESA_NOME}.
Seja simpática, prestativa e use emojis naturalmente.
Seu objetivo é ajudar clientes, tirar dúvidas e facilitar vendas.
Se não souber algo, seja educada e ofereça contato direto.
"""
