"""
analyzer.py

Analisador definitivo de demandas de TI do AvivaHub.
Arquitetura: Regras explícitas + IA assistida (LangChain).
"""

from typing import List, Set

from app.schemas import (
    DemandInput,
    DemandAnalysisOutput,
    TeamRole,
    EffortEstimate
)

from app.catalog import (
    suggest_categories_from_text,
    get_default_roles_for_category
)

from app.llm import run_llm_analysis


# ---------------------------------------------------------
# REGRAS DE NEGÓCIO (GUARDRAILS)
# ---------------------------------------------------------

def _estimate_effort(categories: Set[str]) -> EffortEstimate:
    """
    Estima esforço de forma orientativa.
    A IA NÃO define esforço.
    """

    if "seguranca" in categories:
        return EffortEstimate(
            faixa_semanas="4-8",
            faixa_meses="1-2",
            observacoes="Escopo de segurança depende do nível de maturidade do ambiente"
        )

    if "infraestrutura" in categories:
        return EffortEstimate(
            faixa_semanas="6-10",
            faixa_meses="2-3",
            observacoes="Inclui diagnóstico e implementação incremental"
        )

    if "bot_automacao" in categories:
        return EffortEstimate(
            faixa_semanas="6-8",
            faixa_meses="2",
            observacoes="Automação com integrações simples e regras bem definidas"
        )

    return EffortEstimate(
        faixa_semanas="8-12",
        faixa_meses="2-3",
        observacoes="Produto digital com escopo inicial ainda em validação"
    )


def _build_team(categories: Set[str]) -> List[TeamRole]:
    """
    Monta proposta de time baseada no catálogo.
    """

    team = []
    seen = set()

    for category in categories:
        for role in get_default_roles_for_category(category):
            key = f"{role['papel']}-{role['senioridade']}"
            if key not in seen:
                seen.add(key)
                team.append(
                    TeamRole(
                        papel=role["papel"],
                        senioridade=role["senioridade"],
                        quantidade=1
                    )
                )

    if not team:
        team.append(
            TeamRole(
                papel="Desenvolvedor Full Stack",
                senioridade="Pleno",
                quantidade=2
            )
        )

    return team


# ---------------------------------------------------------
# ANALYZER DEFINITIVO
# ---------------------------------------------------------

class DemandAnalyzer:
    """
    Analyzer definitivo:
    - Regras estruturais continuam sob controle do sistema
    - IA melhora entendimento, linguagem e contexto
    """

    def analyze(self, demand: DemandInput) -> DemandAnalysisOutput:
        """
        Executa análise completa de demanda com apoio de IA.
        """

        # 1️⃣ Classificação inicial por regras
        categories = set(suggest_categories_from_text(demand.texto_demanda))

        if demand.categoria:
            categories.add(demand.categoria)

        if not categories:
            categories.add("produto_digital")

        # 2️⃣ Chamada IA (apenas para entendimento semântico)
        llm_result = run_llm_analysis(
            cliente=demand.cliente,
            texto_demanda=demand.texto_demanda,
            categorias=list(categories),
            restricoes=demand.restricoes or []
        )

        # 3️⃣ Construção de time e esforço (sistema decide)
        team = _build_team(categories)
        effort = _estimate_effort(categories)

        # 4️⃣ Montagem do output final (contrato fechado)
        return DemandAnalysisOutput(
            resumo_executivo=llm_result["resumo_executivo"],
            objetivo_do_cliente=llm_result["objetivo_do_cliente"],
            principais_dores=llm_result["principais_dores"],
            tecnologias_mencionadas=llm_result.get("tecnologias_mencionadas", []),
            proposta_de_time=team,
            estimativa_esforco=effort,
            confianca_geral=llm_result.get("confianca_geral", 0.85)
        )
