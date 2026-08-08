"""
Análise principal — Cleveland (14 variáveis + desfecho).

Dados: heart_disease_uci.csv (somente linhas dataset=Cleveland), recodificados
para os códigos numéricos UCI em heart_cleveland_load.py.

Tabelas para a dissertação (TXT): execute gerar_tabelas_txt.py na mesma pasta.
"""
import pandas as pd
import numpy as np
from scipy.stats import spearmanr, chi2_contingency
import statsmodels.api as sm
from sklearn.metrics import roc_curve, roc_auc_score, brier_score_loss
import matplotlib.pyplot as plt
from heart_cleveland_load import load_cleveland_dataframe, UCI_CSV

# ==========================
# 1. CARREGAR DATASET (Cleveland)
# ==========================

if not UCI_CSV.is_file():
    raise FileNotFoundError(
        f"Arquivo não encontrado: {UCI_CSV}\n"
        "Coloque heart_disease_uci.csv na pasta do projeto."
    )

df, fonte = load_cleveland_dataframe()
print("Fonte dos dados:", fonte)
print("Colunas:", list(df.columns))
print(f"\nAmostra final: {len(df)} pacientes (após remoção de missing em ca/thal/slope)")
print(f"Target: 0 (sem doença) = {(df['target']==0).sum()}, 1 (com doença) = {(df['target']==1).sum()}")

print("\nPrimeiras linhas:")
print(df.head())

print("\nInformações:")
print(df.info())

# ==========================
# 2. ESTATÍSTICA DESCRITIVA
# ==========================

print("\nEstatística descritiva:")
print(df.describe())

# ==========================
# 3. ANÁLISE BIVARIADA
# ==========================

target = "target"

# --------------------------
# 3.1 SPEARMAN (contínuas + ca: contagem ordinal 0-3, vasos corados)
# --------------------------

continuous_vars = [
    "age",
    "trestbps",
    "chol",
    "thalach",
    "oldpeak",
    "ca",
]

print("\n===== CORRELAÇÃO SPEARMAN =====")

for var in continuous_vars:
    corr, p = spearmanr(df[var], df[target])
    print(f"{var} vs target -> Spearman = {corr:.3f}, p-value = {p:.5f}")

# --------------------------
# 3.2 QUI-QUADRADO (variáveis categóricas)
# --------------------------

categorical_vars = [
    "sex",
    "cp",
    "fbs",
    "restecg",
    "exang",
    "slope",
    "thal",
]

print("\n===== TESTE QUI-QUADRADO =====")

for var in categorical_vars:
    tabela = pd.crosstab(df[var], df[target])
    chi2, p, dof, exp = chi2_contingency(tabela)
    print(f"\n{var} vs target")
    print("Chi2 =", chi2)
    print("p-value =", p)

# --------------------------
# 3.3 ODDS RATIO (exemplo: sex)
# --------------------------

print("\n===== ODDS RATIO (exemplo: sex vs target) =====")

tabela = pd.crosstab(df["sex"], df[target])

a = tabela.iloc[1, 1]
b = tabela.iloc[1, 0]
c = tabela.iloc[0, 1]
d = tabela.iloc[0, 0]

odds_ratio = (a * d) / (b * c)

print("Odds Ratio =", odds_ratio)

# ==========================
# 4. ANÁLISE MULTIVARIADA
# ==========================

print("\n===== REGRESSÃO LOGÍSTICA =====")

X_reg = df.drop(columns=["target"])
y_reg = df["target"]

X_reg = sm.add_constant(X_reg)

modelo = sm.Logit(y_reg, X_reg)
resultado = modelo.fit()

print(resultado.summary())

# ==========================
# 5. CURVA ROC
# ==========================

prob = resultado.predict(X_reg)

auc = roc_auc_score(y_reg, prob)
brier = brier_score_loss(y_reg, prob)
prev = float(y_reg.mean())
prob_nulo = np.full(shape=len(y_reg), fill_value=prev)
brier_nulo = brier_score_loss(y_reg, prob_nulo)

print("\nAUC =", auc)
print(f"Brier score (modelo logístico) = {brier:.6f}")
print(
    f"Brier score (referência: probabilidade constante = prevalência {prev:.4f}) = {brier_nulo:.6f}"
)
print(
    "(Quanto menor o Brier, melhor a calibragem combinada com o erro quadrático das probabilidades.)"
)

fpr, tpr, thresholds = roc_curve(y_reg, prob)

plt.plot(fpr, tpr)
plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Curva ROC")
plt.tight_layout()
plt.savefig("curva_roc_dataset3.png", dpi=150)
plt.show()
