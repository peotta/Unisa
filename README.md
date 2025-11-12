# Sistema de registro de entrada e saída com alertas de permanência e intervalo de almoço

## Descrição
Este projeto implementa um sistema simples para registrar **entradas, saídas e intervalos de almoço** de colaboradores em uma pequena empresa. O sistema gera **alertas automáticos** quando:
- o tempo máximo de permanência na empresa é excedido;
- o intervalo de almoço é inferior ao mínimo configurado;
- o colaborador permanece mais de 6 horas sem iniciar o almoço.

A aplicação foi desenvolvida em **Python 3.13** com o framework **FastAPI**, buscando rapidez para implementação e testes, praticidade e portabilidade.

---

## Estrutura de Arquivos

```
registro_ponto/
├─ main.py          # Rotas da API
├─ config.py        # Parâmetros e colaboradores
├─ models.py        # Modelos de dados (Pydantic)
├─ storage.py       # Persistência e agrupamento em JSON
├─ alerts.py        # Módulo de alertas (cálculo e regras)
└─ pontos.json      # Base de dados local (gerada automaticamente)
```

---

## Instalação e Execução

### 1️ Requisitos
- **Python 3.10+** (testado em 3.13)
- `pip` instalado e funcional
- Sistema operacional Linux, Windows ou macOS

---

### 2 Instalar dependências

No terminal, dentro da pasta do projeto:

```bash
pip install --break-system-packages "fastapi[standard]" "uvicorn[standard]"
```

> Para ambiente virtual:
> ```bash
> python3 -m venv .venv
> source .venv/bin/activate
> pip install "fastapi[standard]" "uvicorn[standard]"
> ```

---

### 3 Executar o servidor

Ainda dentro da pasta:

```bash
python3 -m uvicorn main:app --reload
```

Saída esperada:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
<img width="727" height="228" alt="image" src="https://github.com/user-attachments/assets/7622f1e0-3ac2-420f-b331-86ece38cf36a" />

---

### 4️ Acessar a interface de testes

Abra no navegador:

**http://127.0.0.1:8000/docs**

Essa página (Swagger UI) permite testar todos os endpoints.

<img width="893" height="481" alt="image" src="https://github.com/user-attachments/assets/a94b33e4-2ba4-4af3-831e-b80181cf9d53" />



---

## Endpoints Principais

| Método | Rota | Descrição |
|:-------|:------|:-----------|
| **POST** | `/pontos` | Registra entrada, início/fim de almoço ou saída |
| **GET** | `/pontos` | Lista todas as marcações armazenadas |
| **GET** | `/alertas` | Exibe alertas automáticos de permanência e almoço |

---

## Exemplos de Uso

### Registrar Entrada
```json
{
  "colaborador_id": "c001",
  "tipo": "entrada"
}
```

### Registrar Início de Almoço
```json
{
  "colaborador_id": "c001",
  "tipo": "almoco_inicio"
}
```

### Registrar Fim de Almoço
```json
{
  "colaborador_id": "c001",
  "tipo": "almoco_fim"
}
```

### Registrar Saída
```json
{
  "colaborador_id": "c001",
  "tipo": "saida"
}
```

---

### Consultar Alertas
Acesse `/alertas` diretamente ou use:
```
GET /alertas?data=2025-10-26
```

Exemplo de retorno:
```json
[
  {
    "data": "2025-10-26",
    "colaborador_id": "c001",
    "colaborador_nome": "Ana",
    "permanencia_horas": 9.5,
    "alertas": [
      "Almoço de 30 min < mínimo de 60 min."
    ]
  }
]
```

---

## Configurações Importantes (`config.py`)

```python
MAX_PERMANENCIA_HORAS = 10          # limite diário
ALMOCO_MIN_MINUTOS = 60             # tempo mínimo de almoço
ALMOCO_JANELA_INICIO = time(11, 0)  # início permitido
ALMOCO_JANELA_FIM = time(15, 0)     # fim permitido
ALERTA_SEM_ALMOCO_APOS_HORAS = 6    # alerta após 6h sem almoço
```

---

## Licença e Uso Acadêmico
Este projeto foi desenvolvido com fins **educacionais**, como atividade prática do **Projeto Integrador** do curso de Engenharia da Computação.  
O código é de uso livre para estudos e pode ser adaptado para futuras implementações mais robustas (banco de dados, autenticação e relatórios visuais).

---

## Autor
**Laerte Peotta de Melo**
Universidade Santo Amaro – UNISA
