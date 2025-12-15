# Datathon: Passos Mágicos - Machine Learning Engineering

## 1) Visão Geral do Projeto
- **Objetivo**: Desenvolver um modelo preditivo para estimar o risco de defasagem escolar ("Defas") dos estudantes da Associação Passos Mágicos, permitindo intervenções precoces.
- **Solução Proposta**: Pipeline completa de Machine Learning com Random Forest, servida via API REST (FastAPI) e empacotada em Docker. Inclui monitoramento de drift e testes automatizados.
- **Stack Tecnológica**:
  - **Linguagem**: Python 3.9+
  - **Frameworks ML**: scikit-learn, pandas, numpy
  - **API**: FastAPI, Uvicorn
  - **Testes**: pytest
  - **Empacotamento**: Docker
  - **Monitoramento**: JSON logging + Script de análise de drift

## 2) Estrutura do Projeto
```text
├── app/
│   ├── main.py             # Entrypoint da API
│   ├── routes.py           # Definição dos endpoints e logging
│   └── model/              # Modelo treinado (.pkl)
├── src/
│   ├── preprocessing.py    # Limpeza e transformação de dados
│   ├── feature_engineering.py # Criação de features (Média Geral)
│   ├── train.py            # Pipeline de treinamento
│   ├── evaluate.py         # Métricas de avaliação
│   ├── monitoring.py       # Script de visualização de Drift
│   └── utils.py            # Utilitários gerais
├── tests/                  # Testes unitários e de integração
├── logs/                   # Logs de predição para monitoramento
├── Dockerfile              # Arquivo de imagem Docker
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação
```

## 3) Instruções de Deploy

### Pré-requisitos
- Python 3.9 ou superior
- Docker (opcional, para container)

### Instalação Local
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Treine o modelo (Gera o arquivo `app/model/model.pkl`):
   ```bash
   python -m src.train
   ```
3. Inicie a API:
   ```bash
   uvicorn app.main:app --reload
   ```

### Execução via Docker
1. Build da imagem:
   ```bash
   docker build -t passos-magicos-ml .
   ```
2. Executar container:
   ```bash
   docker run -p 8000:8000 passos-magicos-ml
   ```

## 4) Exemplos de Chamadas à API

**Endpoint**: `POST /predict`

**Exemplo via cURL**:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "IAA": 8.5, "IEG": 7.0, "IPS": 7.5, "IDA": 6.0,
  "Matem": 8.0, "Portug": 7.5, "Inglês": 9.0,
  "IPV": 7.5, "IAN": 8.0,
  "Fase_ideal": "Fase 2",
  "Destaque_IEG": "Não", "Destaque_IDA": "Não", "Destaque_IPV": "Não"
}'
```

**Resposta Esperada**:
```json
{
  "prediction": "0",
  "confidence": 0.92,
  "label_description": "Defasagem score (0=OnTrack, <0=Advanced?, >0=Lag)"
}
```

## 5) Etapas do Pipeline de Machine Learning
1. **Pré-processamento (`src/preprocessing.py`)**:
   - Imputação de dados faltantes (Mediana para numéricos, Constante para categóricos).
   - One-Hot Encoding para variáveis categóricas (`Fase ideal`, etc.).
   - Remoção de colunas identificadoras ou com vazamento de dados (`Indicado`, `Atingiu PV`).
2. **Engenharia de Features (`src/feature_engineering.py`)**:
   - Criação da variável `Média_Geral` (Média de Português, Matemática e Inglês).
3. **Treinamento (`src/train.py`)**:
   - Modelo: RandomForestClassifier.
   - Avaliação com métricas de Acurácia, F1-Score e Matriz de Confusão.

## Monitoramento
Para verificar o drift de dados e predições:
```bash
python src/monitoring.py
```
Isso analisará o arquivo `logs/predictions.jsonl`.
