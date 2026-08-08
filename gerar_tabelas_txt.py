"""
Gera tabelas em texto para copiar na dissertação (mesma lógica do dataset3.py).

Usa heart_disease_uci.csv via heart_cleveland_load (Cleveland + códigos UCI).

Saída: tabelas_dissertacao.txt

Uso: python gerar_tabelas_txt.py
"""
import io

import numpy as np
import pandas as pd
from scipy.stats import spearmanr, chi2_contingency
import statsmodels.api as sm
from sklearn.metrics import roc_auc_score, brier_score_loss
from heart_cleveland_load import load_cleveland_dataframe, UCI_CSV


def main():
    if not UCI_CSV.is_file():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {UCI_CSV}\n"
            "Coloque heart_disease_uci.csv na pasta do projeto."
        )

    out = io.StringIO()

    def ln(s=""):
        out.write(s + "\n")

    df, FONTE_DADOS = load_cleveland_dataframe()

    n = len(df)
    n0 = int((df["target"] == 0).sum())
    n1 = int((df["target"] == 1).sum())

    ln("=" * 80)
    ln("TABELAS PARA DISSERTAÇÃO — Heart Disease (subconjunto de 14 variáveis)")
    ln(
        "Desfecho: target = 0 sem doença angiográfica significativa; 1 com doença (num >= 1), quando aplicável."
    )
    ln("Fonte dos dados: " + FONTE_DADOS)
    if "heartdataset" in FONTE_DADOS.lower() or "fallback" in FONTE_DADOS.lower():
        ln()
        ln(
            ">>> ATENÇÃO: Fonte alternativa (não é heart_disease_uci.csv). Confira se bate com sua análise."
        )
    ln("=" * 80)
    ln()

    # ----- Tabela 1 -----
    ln("TABELA 1. Características da amostra (N = " + str(n) + ")")
    ln("-" * 80)
    ln(f"Total de participantes\t{n}")
    ln(f"Sem doença (target = 0)\t{n0} ({100 * n0 / n:.1f}%)")
    ln(f"Com doença (target = 1)\t{n1} ({100 * n1 / n:.1f}%)")
    ln()
    ln("Variáveis contínuas — média (desvio padrão)")
    ln("Variável\tMédia\tDP")
    for col in ["age", "trestbps", "chol", "thalach", "oldpeak", "ca"]:
        ln(f"{col}\t{df[col].mean():.2f}\t{df[col].std():.2f}")
    ln()
    ln("Variáveis categóricas — n (%) do total da amostra")
    for col in ["sex", "cp", "fbs", "restecg", "exang", "slope", "thal"]:
        vc = df[col].value_counts().sort_index()
        for k, v in vc.items():
            ln(f"{col} = {k}\t{v} ({100 * v / n:.1f}%)")
        ln()

    # ----- Tabela 2 -----
    ln("=" * 80)
    ln("TABELA 2. Correlação de Spearman com o desfecho (target)")
    ln("-" * 80)
    ln("Variável\trho\tp-valor")
    continuous_vars = ["age", "trestbps", "chol", "thalach", "oldpeak", "ca"]
    for var in continuous_vars:
        corr, p = spearmanr(df[var], df["target"])
        ln(f"{var}\t{corr:.4f}\t{p:.6g}")
    ln()

    # ----- Tabela 3 -----
    ln("=" * 80)
    ln("TABELA 3. Teste qui-quadrado de independência (variável × target)")
    ln("-" * 80)
    ln("Variável\tQui-quadrado\tGraus de liberdade\tp-valor")
    categorical_vars = ["sex", "cp", "fbs", "restecg", "exang", "slope", "thal"]
    for var in categorical_vars:
        tab = pd.crosstab(df[var], df["target"])
        chi2, p, dof, _ = chi2_contingency(tab)
        ln(f"{var}\t{chi2:.6f}\t{dof}\t{p:.6g}")
    ln()

    # ----- OR bruto sexo -----
    ln("=" * 80)
    ln("TABELA 3b (opcional). Contingência sexo × target e odds ratio bruto")
    ln("-" * 80)
    tabela = pd.crosstab(df["sex"], df["target"])
    ln("(Linhas: sexo 0=feminino, 1=masculino; Colunas: target 0, 1)")
    ln(tabela.to_string())
    ln()
    a = tabela.iloc[1, 1]
    b = tabela.iloc[1, 0]
    c = tabela.iloc[0, 1]
    d = tabela.iloc[0, 0]
    or_sex = (a * d) / (b * c)
    ln(f"Odds ratio (masculino vs feminino, bruto)\t{or_sex:.6f}")
    ln()

    # ----- Tabela 4 -----
    X_reg = sm.add_constant(df.drop(columns=["target"]))
    y_reg = df["target"]
    res = sm.Logit(y_reg, X_reg).fit(disp=0)
    ci = res.conf_int()
    ci.columns = ["ic_inf", "ic_sup"]

    ln("=" * 80)
    ln("TABELA 4. Regressão logística multivariada (coeficientes e OR ajustados)")
    ln("-" * 80)
    ln(
        "Variável\tCoeficiente\tErro padrão\tz\tp-valor\tOR\tIC95% OR (inf)\tIC95% OR (sup)"
    )
    for name in res.params.index:
        b = res.params[name]
        se = res.bse[name]
        z = res.tvalues[name]
        p = res.pvalues[name]
        or_ = np.exp(b)
        lo = np.exp(ci.loc[name, "ic_inf"])
        hi = np.exp(ci.loc[name, "ic_sup"])
        ln(
            f"{name}\t{b:.6f}\t{se:.6f}\t{z:.4f}\t{p:.6g}\t{or_:.6f}\t{lo:.6f}\t{hi:.6f}"
        )
    ln()
    ln(f"Pseudo R² (McFadden)\t{res.prsquared:.6f}")
    ln(f"Log-likelihood\t{res.llf:.4f}")
    ln(f"Teste LR (modelo vs. intercepto apenas), p-valor\t{res.llr_pvalue:.6g}")
    ln()

    # ----- Tabela 5 -----
    prob = res.predict(X_reg)
    auc = roc_auc_score(y_reg, prob)
    brier = brier_score_loss(y_reg, prob)
    prev = float(y_reg.mean())
    prob_nulo = np.full(shape=len(y_reg), fill_value=prev)
    brier_nulo = brier_score_loss(y_reg, prob_nulo)
    ln("=" * 80)
    ln("TABELA 5 / Figura — Desempenho discriminativo (amostra completa, in-sample)")
    ln("-" * 80)
    ln(f"AUC (área sob a curva ROC)\t{auc:.6f}")
    ln(f"Brier score (modelo logístico)\t{brier:.6f}")
    ln(f"Brier score (referência: só prevalência = {prev:.4f})\t{brier_nulo:.6f}")
    ln(
        "Nota: AUC e Brier na mesma amostra do ajuste (otimistas para generalização). "
        "Brier menor = melhor; comparar com o modelo nulo."
    )
    ln()

    texto = out.getvalue()
    path = "tabelas_dissertacao.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"Arquivo gerado: {path} ({len(texto)} caracteres)")


if __name__ == "__main__":
    main()
