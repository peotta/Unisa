from typing import List, Dict
from datetime import datetime
import json, os

from models import MarcacaoStore

ARQ = "pontos.json"

def carregar() -> List[MarcacaoStore]:
    if not os.path.exists(ARQ):
        return []
    with open(ARQ, "r", encoding="utf-8") as f:
        raw = json.load(f)
    for r in raw:
        r["timestamp"] = datetime.fromisoformat(r["timestamp"])
    return [MarcacaoStore(**r) for r in raw]

def salvar(items: List[MarcacaoStore]) -> None:
    serial = []
    for i in items:
        d = i.dict()
        d["timestamp"] = d["timestamp"].isoformat()
        serial.append(d)
    with open(ARQ, "w", encoding="utf-8") as f:
        json.dump(serial, f, ensure_ascii=False, indent=2)

def grouper_por_colab_dia(marcs: List[MarcacaoStore]) -> Dict[str, Dict[str, List[MarcacaoStore]]]:
    """
    Agrupa como {colab_id: {YYYY-MM-DD: [marcacoes...]}} e ordena por horário.
    """
    out: Dict[str, Dict[str, List[MarcacaoStore]]] = {}
    for m in marcs:
        dia = m.timestamp.date().isoformat()
        out.setdefault(m.colaborador_id, {}).setdefault(dia, []).append(m)
    for colab in out:
        for dia in out[colab]:
            out[colab][dia].sort(key=lambda x: x.timestamp)
    return out
