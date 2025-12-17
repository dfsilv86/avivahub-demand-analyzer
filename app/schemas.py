  # Configurações (env / parâmetros)
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


# ---------------------------------------------------------
# ENUMS
# ---------------------------------------------------------

class UrgencyLevel(str, Enum):
    """
    Representa a urgência percebida da demanda.

    Importante:
    - É percepção do comercial/pré-venda
    - NÃO é SLA
    - NÃO é compromisso de prazo
    """
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


# ---------------------------------------------------------
# INPUT DO AGENTE
# ---------------------------------------------------------

class DemandInput(BaseModel):
    """
    Representa a entrada bruta da análise de demanda.

    Essa classe modela exatamente o que vem da tela de input
    ou de uma API externa. Ela deve ser simples, tolerante
    e focada em texto humano.
    """

    cliente: str = Field(
        ...,
        description="Nome do prospect ou cliente",
        examples=["Hospital São Lucas"]
    )

    texto_demanda: str = Field(
        ...,
        description=(
            "Descrição livre da demanda do cliente. "
            "Texto não técnico, geralmente vindo de uma conversa comercial."
        ),
        examples=[
            "Cliente quer desenvolver um aplicativo para acompanhar chamados internos."
        ]
    )

    categoria: Optional[str] = Field(
        None,
        description=(
            "Categoria percebida da demanda. "
            "Ex: produto_digital, bot, seguranca, infraestrutura. "
            "Pode ser omitida se o usuário não souber."
        )
    )

    restricoes: Optional[List[str]] = Field(
        default_factory=list,
        description=(
            "Lista de restrições conhecidas informadas pelo cliente ou percebidas "
            "pelo comercial (LGPD, prazo curto, sistema legado, etc.)"
        )
    )

    urgencia: Optional[UrgencyLevel] = Field(
        UrgencyLevel.MEDIA,
        description="Urgência percebida da demanda"
    )


# ---------------------------------------------------------
# MODELOS DE APOIO À SAÍDA
# ---------------------------------------------------------

class TeamRole(BaseModel):
    """
    Representa UM papel dentro da proposta de time.

    Essa estrutura permite que o agente sugira times
    de forma clara, explícita e fácil de evoluir.
    """

    papel: str = Field(
        ...,
        description="Nome do papel (ex: Desenvolvedor Backend, SRE, Analista de Segurança)"
    )

    senioridade: str = Field(
        ...,
        description="Senioridade sugerida (Júnior, Pleno, Sênior, Especialista)"
    )

    quantidade: int = Field(
        ...,
        ge=1,
        description="Quantidade de pessoas nesse papel"
    )


class EffortEstimate(BaseModel):
    """
    Representa a estimativa de esforço da demanda.

    IMPORTANTE:
    - Sempre orientativa
    - Nunca contratual
    - Sempre em semanas e meses
    """

    faixa_semanas: str = Field(
        ...,
        description="Faixa estimada em semanas (ex: 8-12)"
    )

    faixa_meses: str = Field(
        ...,
        description="Faixa estimada em meses (ex: 2-3)"
    )

    observacoes: Optional[str] = Field(
        None,
        description=(
            "Observações ou pressupostos usados para a estimativa "
            "(ex: depende de integrações, escopo ainda não validado)"
        )
    )


# ---------------------------------------------------------
# OUTPUT FINAL DO AGENTE
# ---------------------------------------------------------

class DemandAnalysisOutput(BaseModel):
    """
    Representa o RESULTADO FINAL da análise de demanda.

    Esse é o JSON que o agente SEMPRE deve retornar.
    Ele alimenta dashboards, histórico e decisões.
    """

    resumo_executivo: str = Field(
        ...,
        description=(
            "Resumo executivo da análise (3 a 4 linhas), "
            "em linguagem clara para decisão."
        )
    )

    objetivo_do_cliente: str = Field(
        ...,
        description="Objetivo principal que o cliente deseja atingir"
    )

    principais_dores: List[str] = Field(
        ...,
        description=(
            "Lista das principais dores identificadas na fala do cliente. "
            "Deve ser objetiva e direta."
        )
    )

    tecnologias_mencionadas: List[str] = Field(
        default_factory=list,
        description=(
            "Tecnologias, plataformas ou termos técnicos citados explicitamente "
            "na demanda (ex: AWS, Kubernetes, WhatsApp, SOC)."
        )
    )

    proposta_de_time: List[TeamRole] = Field(
        ...,
        description=(
            "Proposta de time sugerida para atender a demanda, "
            "informando papéis, senioridades e quantidades."
        )
    )

    estimativa_esforco: EffortEstimate = Field(
        ...,
        description="Estimativa orientativa de esforço"
    )

    confianca_geral: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description=(
            "Nível de confiança da análise (0 a 1). "
            "Quanto maior, maior a segurança do agente."
        )
    )
