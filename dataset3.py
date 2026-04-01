import pandas as pd
import numpy as np
from scipy.stats import spearmanr, chi2_contingency
import statsmodels.api as sm
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from ucimlrepo import fetch_ucirepo

# ==========================
# 1. CARREGAR DATASET (UCI)
# ==========================

heart_disease = fetch_ucirepo(id=45)

X = heart_disease.data.features
y = heart_disease.data.targets

df = pd.concat([X, y], axis=1)

print("Colunas originais:", list(df.columns))
print(f"Total bruto: {len(df)} pacientes")
print(f"\nMissing por coluna:")
print(df.isnull().sum())

df["target"] = (df["num"] >= 1).astype(int)
df = df.drop(columns=["num"])

df = df.dropna()
df = df.reset_index(drop=True)

print(f"\nAmostra final: {len(df)} pacientes (após remoção de missing values)")
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

print("\nAUC =", auc)

fpr, tpr, thresholds = roc_curve(y_reg, prob)

plt.plot(fpr, tpr)
plt.plot([0, 1], [0, 1])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Curva ROC")
plt.show()
