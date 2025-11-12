from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from models import MarcacaoStore
from storage import grouper_por_colab_dia
from config import (
    MAX_PERMANENCIA_HORAS,
    ALMOCO_MIN_MINUTOS,
    ALMOCO_JANELA_INICIO,
    ALMOCO_JANELA_FIM,
    ALERTA_SEM_ALMOCO_APOS_HORAS,
    COLABORADORES,
)

def calcular_alertas(marcs: List[MarcacaoStore], data_alvo: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Calcula alertas por colaborador para a 'data_alvo' (YYYY-MM-DD).
    Se data_alvo=None, usa a data de hoje.
    """
    grupos = grouper_por_colab_dia(marcs)
    hoje_str = datetime.now().date().isoformat()
    alvo = data_alvo or hoje_str

    resultados: List[Dict[str, Any]] = []
    for colab_id, dias in grupos.items():
        if alvo not in dias:
            continue

        pontos = dias[alvo]
        nome = COLABORADORES.get(colab_id, colab_id)

        entrada = next((p for p in pontos if p.tipo == "entrada"), None)
        saida = next((p for p in reversed(pontos) if p.tipo == "saida"), None)
        alm_i = next((p for p in pontos if p.tipo == "almoco_inicio"), None)
        alm_f = next((p for p in pontos if p.tipo == "almoco_fim"), None)

        avisos: List[str] = []
        permanencia_horas: Optional[float] = None

        # 1) 6h sem almoço
        if entrada and not alm_i:
            if alvo == hoje_str:
                decorrido = datetime.now() - entrada.timestamp
            else:
                decorrido = (saida.timestamp - entrada.timestamp) if saida else timedelta(0)
            if decorrido >= timedelta(hours=ALERTA_SEM_ALMOCO_APOS_HORAS):
                avisos.append(f"Mais de {ALERTA_SEM_ALMOCO_APOS_HORAS}h desde a entrada sem início de almoço.")

        # 2) Permanência diária
        permanencia = None
        if entrada and saida:
            permanencia = saida.timestamp - entrada.timestamp
            if alm_i and alm_f and alm_f.timestamp > alm_i.timestamp:
                permanencia -= (alm_f.timestamp - alm_i.timestamp)
            permanencia_horas = round(permanencia.total_seconds()/3600, 2)
            if permanencia > timedelta(hours=MAX_PERMANENCIA_HORAS):
                avisos.append(f"Permanência {permanencia_horas}h > limite de {MAX_PERMANENCIA_HORAS}h.")

        # 3) Almoço mínimo e janela
        if alm_i and alm_f and alm_f.timestamp > alm_i.timestamp:
            intervalo = alm_f.timestamp - alm_i.timestamp
            if intervalo < timedelta(minutes=ALMOCO_MIN_MINUTOS):
                mins = int(intervalo.total_seconds()/60)
                avisos.append(f"Almoço de {mins} min < mínimo de {ALMOCO_MIN_MINUTOS} min.")
            h_i, h_f = alm_i.timestamp.time(), alm_f.timestamp.time()
            if not (ALMOCO_JANELA_INICIO <= h_i <= ALMOCO_JANELA_FIM and ALMOCO_JANELA_INICIO <= h_f <= ALMOCO_JANELA_FIM):
                avisos.append("Almoço fora da janela 11:00–15:00.")
        else:
            if entrada and (saida or alvo == hoje_str):
                avisos.append("Almoço ausente ou incompleto (sem início/fim).")

        resultados.append({
            "data": alvo,
            "colaborador_id": colab_id,
            "colaborador_nome": nome,
            "permanencia_horas": permanencia_horas,
            "alertas": avisos or ["Sem alertas."]
        })

    return resultados
