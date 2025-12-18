# Catálogo de serviços, papéis e regras
"""
catalog.py

Catálogo de serviços de TI, papéis e padrões de time
usados pelo Analisador de Demandas do AvivaHub.

Este arquivo NÃO contém lógica de IA.
Ele representa conhecimento explícito do domínio.
"""

from typing import Dict, List


# ---------------------------------------------------------
# TIPOS DE SERVIÇO SUPORTADOS PELO AGENTE
# ---------------------------------------------------------

# Chaves simples, estáveis e fáceis de versionar
SERVICE_CATEGORIES: Dict[str, Dict] = {
    "produto_digital": {
        "descricao": "Desenvolvimento de produtos digitais como sistemas, plataformas e aplicações web/mobile",
        "papeis_padrao": [
            {"papel": "Tech Lead", "senioridade": "Sênior"},
            {"papel": "Desenvolvedor Backend", "senioridade": "Pleno/Sênior"},
            {"papel": "Desenvolvedor Frontend", "senioridade": "Pleno"},
            {"papel": "QA", "senioridade": "Pleno"}
        ],
        "observacoes": (
            "Normalmente envolve levantamento de requisitos, "
            "integrações e ciclos iterativos de entrega."
        )
    },

    "bot_automacao": {
        "descricao": "Desenvolvimento de bots, automações e assistentes (ex: WhatsApp, chatbots, RPA)",
        "papeis_padrao": [
            {"papel": "Desenvolvedor Backend", "senioridade": "Pleno"},
            {"papel": "Especialista em IA/Automação", "senioridade": "Sênior"}
        ],
        "observacoes": (
            "Escopo geralmente menor, mas depende fortemente "
            "da clareza de regras e integrações."
        )
    },

    "infraestrutura": {
        "descricao": "Serviços de infraestrutura, cloud, DevOps e confiabilidade",
        "papeis_padrao": [
            {"papel": "Arquiteto de Infraestrutura", "senioridade": "Sênior"},
            {"papel": "DevOps / SRE", "senioridade": "Pleno/Sênior"}
        ],
        "observacoes": (
            "Costuma envolver análise de ambiente existente, "
            "custos de cloud e automação de provisionamento."
        )
    },

    "seguranca": {
        "descricao": "Serviços de segurança da informação (SOC, Pentest, hardening, compliance)",
        "papeis_padrao": [
            {"papel": "Especialista em Segurança", "senioridade": "Sênior"},
            {"papel": "Analista de Segurança", "senioridade": "Pleno"}
        ],
        "observacoes": (
            "Normalmente envolve requisitos regulatórios, "
            "documentação e validações formais."
        )
    }
}


# ---------------------------------------------------------
# PALAVRAS-CHAVE PARA AJUDAR NA CLASSIFICAÇÃO
# ---------------------------------------------------------

# Isso NÃO substitui o LLM.
# Serve como sinal auxiliar para orientar a análise.
KEYWORDS_TO_CATEGORY: Dict[str, str] = {
    # Produto / Software
    "sistema": "produto_digital",
    "aplicativo": "produto_digital",
    "app": "produto_digital",
    "plataforma": "produto_digital",
    "software": "produto_digital",

    # Bots / Automação
    "bot": "bot_automacao",
    "chatbot": "bot_automacao",
    "whatsapp": "bot_automacao",
    "automação": "bot_automacao",
    "rpa": "bot_automacao",

    # Infraestrutura
    "cloud": "infraestrutura",
    "aws": "infraestrutura",
    "azure": "infraestrutura",
    "kubernetes": "infraestrutura",
    "devops": "infraestrutura",

    # Segurança
    "segurança": "seguranca",
    "pentest": "seguranca",
    "soc": "seguranca",
    "lgpd": "seguranca",
    "compliance": "seguranca"
}


# ---------------------------------------------------------
# FUNÇÕES AUXILIARES (SIMPLES E EXPLÍCITAS)
# ---------------------------------------------------------

def suggest_categories_from_text(texto: str) -> List[str]:
    """
    Sugere categorias de serviço com base em palavras-chave
    encontradas no texto da demanda.

    Importante:
    - Retorna sugestões, não decisões finais
    - Pode retornar múltiplas categorias
    """

    texto_lower = texto.lower()
    categorias_encontradas = set()

    for keyword, categoria in KEYWORDS_TO_CATEGORY.items():
        if keyword in texto_lower:
            categorias_encontradas.add(categoria)

    return list(categorias_encontradas)


def get_default_roles_for_category(categoria: str) -> List[Dict[str, str]]:
    """
    Retorna os papéis padrão associados a uma categoria de serviço.

    Se a categoria não existir, retorna lista vazia.
    """
    categoria_info = SERVICE_CATEGORIES.get(categoria)
    if not categoria_info:
        return []
    return categoria_info.get("papeis_padrao", [])


def get_category_description(categoria: str) -> str:
    """
    Retorna a descrição textual da categoria de serviço.
    """
    categoria_info = SERVICE_CATEGORIES.get(categoria)
    if not categoria_info:
        return ""
    return categoria_info.get("descricao", "")
