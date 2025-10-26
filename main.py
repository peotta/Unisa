"""
como rodar o programa
pip install --break-system-packages "fastapi[standard]" "uvicorn[standard]"
python3 -m uvicorn main:app --reload
"""


from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from datetime import datetime

from models import Marcacao, MarcacaoStore
from storage import carregar, salvar
from alerts import calcular_alertas
from config import COLABORADORES

app = FastAPI(title="Registro de Entrada/Saída - Empresa Pequena")

@app.get("/pontos", response_model=List[MarcacaoStore])
def listar_pontos():
    return carregar()

@app.post("/pontos", response_model=MarcacaoStore, status_code=201)
def criar_ponto(m: Marcacao):
    if m.colaborador_id not in COLABORADORES:
        raise HTTPException(400, "Colaborador inexistente")

    marcs = carregar()
    novo_id = (max([x.id for x in marcs]) + 1) if marcs else 1
    if m.timestamp is None:
        m.timestamp = datetime.now()

    # Validação de sequência mínima por dia
    dia = m.timestamp.date().isoformat()
    do_dia = [x for x in marcs if x.colaborador_id == m.colaborador_id and x.timestamp.date().isoformat() == dia]
    do_dia.sort(key=lambda x: x.timestamp)
    tipos = [x.tipo for x in do_dia]

    if m.tipo == "almoco_fim" and "almoco_inicio" not in tipos:
        raise HTTPException(400, "Não é possível finalizar almoço sem ter iniciado")
    if m.tipo == "saida" and "entrada" not in tipos:
        raise HTTPException(400, "Não é possível registrar saída sem entrada")

    store = MarcacaoStore(id=novo_id, **m.dict())
    marcs.append(store)
    salvar(marcs)
    return store

@app.get("/alertas")
def alertas(data: Optional[str] = Query(None, description="YYYY-MM-DD, opcional")):
    marcs = carregar()
    return calcular_alertas(marcs, data)
