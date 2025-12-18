# Integração LangChain / LLM
"""
llm.py

Camada de integração com LLM (LangChain) para o
Analisador de Demandas do AvivaHub.

Responsabilidade única:
- Executar análise semântica
- Retornar JSON estruturado e validado
"""

from typing import Dict, List

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from pydantic import BaseModel, Field

from app.config import settings
from app.prompt import SYSTEM_PROMPT, USER_PROMPT


# ---------------------------------------------------------
# SCHEMA DE SAÍDA DO LLM (RESTRITO)
# ---------------------------------------------------------

class LLMAnalysisResult(BaseModel):
    """
    Resultado que o LLM está AUTORIZADO a retornar.

    Esse schema é intencionalmente limitado para
    evitar que a IA tome decisões estruturais.
    """

    resumo_executivo: str = Field(
        ...,
        description="Resumo executivo da análise (3-4 linhas)"
    )

    objetivo_do_cliente: str = Field(
        ...,
        description="Objetivo principal do cliente"
    )

    principais_dores: List[str] = Field(
        ...,
        description="Lista objetiva das principais dores identificadas"
    )

    tecnologias_mencionadas: List[str] = Field(
        default_factory=list,
        description="Tecnologias explicitamente mencionadas no texto"
    )

    confianca_geral: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confiança da análise (0 a 1)"
    )


# ---------------------------------------------------------
# CLIENTE LLM
# ---------------------------------------------------------

def _build_llm() -> ChatOpenAI:
    """
    Constrói o cliente LangChain do LLM.

    Centralizar isso facilita:
    - trocar modelo
    - trocar provider
    - ajustar parâmetros
    """

    return ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        timeout=settings.LLM_TIMEOUT_SECONDS,
        max_retries=settings.LLM_MAX_RETRIES,
        api_key=settings.OPENAI_API_KEY
    )


# ---------------------------------------------------------
# FUNÇÃO PÚBLICA DO MÓDULO
# ---------------------------------------------------------

def run_llm_analysis(
    cliente: str,
    texto_demanda: str,
    categorias: List[str],
    restricoes: List[str]
) -> Dict:
    """
    Executa a análise semântica via LLM.

    IMPORTANTE:
    - Essa função NÃO define time ou prazo
    - Apenas entende o texto humano
    """

    llm = _build_llm()

    parser = PydanticOutputParser(
        pydantic_object=LLMAnalysisResult
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", USER_PROMPT)
    ]).partial(
        format_instructions=parser.get_format_instructions()
    )

    chain = prompt | llm | parser

    result: LLMAnalysisResult = chain.invoke({
        "cliente": cliente,
        "texto_demanda": texto_demanda,
        "categorias": ", ".join(categorias),
        "restricoes": ", ".join(restricoes) if restricoes else "Nenhuma"
    })

    return result.model_dump()
