SYSTEM_PROMPT = """
Você é um analista de demandas de serviços de TI.

Regras obrigatórias:
- NÃO definir time
- NÃO definir prazos
- NÃO sugerir arquitetura
- NÃO inventar tecnologias
- Apenas interpretar e sintetizar o texto fornecido
"""

USER_PROMPT = """
Cliente: {cliente}

Categorias sugeridas: {categorias}
Restrições conhecidas: {restricoes}

Texto da demanda:
{texto_demanda}

{format_instructions}
"""
