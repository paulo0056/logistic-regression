"""
Carrega o subconjunto Cleveland (14 variáveis + num) com codificação numérica UCI.

Prioridade:
  1) heart_disease_uci.csv (filtra dataset=Cleveland, recodifica texto → códigos UCI)
  2) ucimlrepo id=45
  3) heartdataset.csv (já numérico)
"""
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
# Caminho absoluto exportável para checagem em dataset3.py
UCI_CSV = BASE / "heart_disease_uci.csv"
KAGGLE_CSV = BASE / "heartdataset.csv"


def _from_uci_export(raw: pd.DataFrame) -> pd.DataFrame:
    d = raw.loc[raw["dataset"].astype(str).str.strip() == "Cleveland"].copy()
    if len(d) == 0:
        raise ValueError("Nenhuma linha Cleveland em heart_disease_uci.csv")

    # CSV export: coluna 'thalch' → nome padrão UCI 'thalach'
    d.columns = ["thalach" if c == "thalch" else c for c in d.columns]

    sex_m = {"male": 1, "female": 0}
    cp_m = {
        "typical angina": 1,
        "atypical angina": 2,
        "non-anginal": 3,
        "asymptomatic": 4,
    }
    rest_m = {"normal": 0, "st-t abnormality": 1, "lv hypertrophy": 2}
    slope_m = {"upsloping": 1, "flat": 2, "downsloping": 3}
    thal_m = {"normal": 3, "fixed defect": 6, "reversable defect": 7, "reversible defect": 7}

    def norm(x):
        if pd.isna(x):
            return x
        return str(x).strip().lower()

    d["sex"] = d["sex"].map(lambda x: sex_m.get(norm(x), x))
    d["cp"] = d["cp"].map(lambda x: cp_m.get(norm(x), x))
    d["fbs"] = d["fbs"].map(lambda x: 1 if x is True or str(x).upper() == "TRUE" else 0)
    d["restecg"] = d["restecg"].map(lambda x: rest_m.get(norm(x), x))
    d["exang"] = d["exang"].map(lambda x: 1 if x is True or str(x).upper() == "TRUE" else 0)
    d["slope"] = d["slope"].map(lambda x: slope_m.get(norm(x), x) if pd.notna(x) else x)
    d["thal"] = d["thal"].map(lambda x: thal_m.get(norm(x), x) if pd.notna(x) else x)
    d["ca"] = pd.to_numeric(d["ca"], errors="coerce")

    cols = [
        "age",
        "sex",
        "cp",
        "trestbps",
        "chol",
        "fbs",
        "restecg",
        "thalach",
        "exang",
        "oldpeak",
        "slope",
        "ca",
        "thal",
        "num",
    ]
    d = d[cols].copy()
    d["target"] = (d["num"] >= 1).astype(int)
    d = d.drop(columns=["num"])
    d = d.dropna().reset_index(drop=True)

    for c in ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "slope", "thal"]:
        d[c] = d[c].astype(int)
    d["ca"] = d["ca"].astype(float)
    d["oldpeak"] = d["oldpeak"].astype(float)

    return d


def load_cleveland_dataframe():
    """
    Retorna (DataFrame pronto para análise, descrição da fonte).
    Colunas finais: 13 preditoras + target (0/1).
    """
    if UCI_CSV.is_file():
        raw = pd.read_csv(UCI_CSV)
        d = _from_uci_export(raw)
        return (
            d,
            f"Arquivo local {UCI_CSV.name} (apenas Cleveland, codificação numérica UCI, após dropna em ca/thal/slope)",
        )

    try:
        from ucimlrepo import fetch_ucirepo

        heart_disease = fetch_ucirepo(id=45)
        d = pd.concat([heart_disease.data.features, heart_disease.data.targets], axis=1)
        d["target"] = (d["num"] >= 1).astype(int)
        d = d.drop(columns=["num"]).dropna().reset_index(drop=True)
        return d, "UCI ML Repository (ucimlrepo, id=45), após dropna em ca/thal"
    except Exception:
        pass

    if not KAGGLE_CSV.is_file():
        raise FileNotFoundError(
            "Coloque heart_disease_uci.csv na pasta do projeto ou instale ucimlrepo com rede."
        )

    d = pd.read_csv(KAGGLE_CSV)
    if "num" in d.columns:
        d["target"] = (d["num"] >= 1).astype(int)
        d = d.drop(columns=["num"])
    d = d.dropna().reset_index(drop=True)
    return (
        d,
        f"Arquivo local {KAGGLE_CSV.name} (fallback — codificação pode diferir do Cleveland UCI)",
    )
