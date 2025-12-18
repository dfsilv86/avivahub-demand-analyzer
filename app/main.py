# FastAPI app + endpoints
"""
main.py

API FastAPI do AvivaHub Demand Analyzer.
Responsável por expor endpoints HTTP e delegar a análise ao DemandAnalyzer.

Importante:
- Aqui NÃO fica lógica de negócio do agente.
- Aqui fica apenas orquestração HTTP (entrada/saída, validação, erros, CORS).
"""

import time
import uuid
import logging
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.schemas import DemandInput, DemandAnalysisOutput
from app.analyzer import DemandAnalyzer

# ---------------------------------------------------------
# LOGGING BÁSICO
# ---------------------------------------------------------

logger = logging.getLogger("avivahub-demand-analyzer")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

# ---------------------------------------------------------
# APP FASTAPI
# ---------------------------------------------------------

app = FastAPI(
    title="AvivaHub - Demand Analyzer",
    version="1.0.0",
    description="API para análise de demandas de pré-venda de serviços de TI (produto digital, bots, segurança, infraestrutura)."
)

# ---------------------------------------------------------
# CORS (AJUSTE PARA SEU AMBIENTE)
# ---------------------------------------------------------
# Em produção, restrinja para o domínio do seu front.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # ex: ["http://localhost:4200"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# DEPENDÊNCIA PRINCIPAL (SIMPLES)
# ---------------------------------------------------------

analyzer = DemandAnalyzer()


# ---------------------------------------------------------
# MIDDLEWARE: REQUEST ID + TEMPO
# ---------------------------------------------------------

@app.middleware("http")
async def add_request_id_and_timing(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    request.state.request_id = request_id

    start = time.time()
    response = await call_next(request)
    elapsed_ms = int((time.time() - start) * 1000)

    response.headers["x-request-id"] = request_id
    response.headers["x-response-time-ms"] = str(elapsed_ms)

    return response


# ---------------------------------------------------------
# HANDLERS DE ERRO (PADRONIZA SAÍDA)
# ---------------------------------------------------------

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """
    Handler global para erros inesperados.
    Retorna JSON padronizado e loga com request_id.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    logger.exception("Unhandled error request_id=%s path=%s", request_id, request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "Ocorreu um erro inesperado ao processar a demanda.",
            "request_id": request_id
        }
    )


# ---------------------------------------------------------
# ENDPOINTS
# ---------------------------------------------------------

@app.get("/health")
def health() -> Dict[str, Any]:
    """
    Healthcheck simples para validar que o serviço está no ar.
    """
    return {"status": "ok", "service": "avivahub-demand-analyzer"}


@app.post("/analyze-demand", response_model=DemandAnalysisOutput)
async def analyze_demand(payload: DemandInput, request: Request) -> DemandAnalysisOutput:
    """
    Executa a análise de demanda.

    Entrada:
    - DemandInput (cliente, texto_demanda, categoria opcional, restrições, urgência)

    Saída:
    - DemandAnalysisOutput (JSON estruturado para dashboard)
    """
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(
        "analyze-demand.start request_id=%s cliente=%s categoria=%s urgencia=%s",
        request_id, payload.cliente, payload.categoria, payload.urgencia
    )

    result = analyzer.analyze(payload)

    logger.info(
        "analyze-demand.done request_id=%s cliente=%s confianca=%.2f",
        request_id, payload.cliente, result.confianca_geral
    )

    return result
