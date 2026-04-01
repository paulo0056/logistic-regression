import pandas as pd
import numpy as np
from scipy.stats import spearmanr, chi2_contingency
import statsmodels.api as sm
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt

# ==========================
# 1. CARREGAR DATASET
# ==========================

df = pd.read_csv("data.csv")

print(f"Amostra: {len(df)} pacientes")
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
# 3.1 SPEARMAN (variáveis contínuas)
# --------------------------

continuous_vars = [
    "age",
    "trestbps",
    "chol",
    "thalach",
    "oldpeak"
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
    "ca",
    "thal"
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

a = tabela.iloc[1,1]
b = tabela.iloc[1,0]
c = tabela.iloc[0,1]
d = tabela.iloc[0,0]

odds_ratio = (a * d) / (b * c)

print("Odds Ratio =", odds_ratio)

# ==========================
# 4. ANÁLISE MULTIVARIADA
# ==========================

print("\n===== REGRESSÃO LOGÍSTICA =====")

X = df.drop(columns=["target"])
y = df["target"]

X = sm.add_constant(X)

modelo = sm.Logit(y, X)
resultado = modelo.fit()

print(resultado.summary())

# ==========================
# 5. CURVA ROC
# ==========================

prob = resultado.predict(X)

auc = roc_auc_score(y, prob)

print("\nAUC =", auc)

fpr, tpr, thresholds = roc_curve(y, prob)

plt.plot(fpr, tpr)
plt.plot([0, 1], [0, 1])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Curva ROC")
plt.show()