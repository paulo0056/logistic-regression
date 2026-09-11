# Dissertação de mestrado (rascunho em Markdown)

**Título provisório:** Associação entre variáveis clínicas e presença de doença cardíaca: análise bivariada e regressão logística no subconjunto Cleveland (UCI)

**Norma de estrutura:** ABNT NBR 14724.  
**Arquivo:** rascunho para Word/LaTeX. Substituir os campos entre colchetes antes da versão oficial.

---

## Recado de trabalho (não entra no PDF da defesa)

Este ficheiro, nesta etapa, contém **apenas** os elementos pré-textuais e as tabelas metodológicas pedidas pelo orientador. Os capítulos 1 a 5 e as referências Scopus ainda não foram redigidos.

**O que o projeto analítico já atende**

- Dados secundários, públicos e anonimizados do UCI (subconjunto Cleveland), N = 297 após exclusão de valores em falta em `ca`, `thal` e `slope`.
- Desfecho binário (`target` = 0 sem doença angiográfica significativa; 1 com doença).
- Treze preditoras clássicas no modelo logístico (não se reduz o Logit a cinco variáveis).
- Bivariada: Spearman, qui-quadrado e OR bruto de sexo.
- Multivariada: regressão logística binária, teste de razão de verossimilhança (H0 global).
- Desempenho: curva ROC / AUC e Brier score versus modelo nulo de prevalência constante.
- Código reprodutível: `dataset3.py`, `heart_cleveland_load.py`, `gerar_tabelas_txt.py`.

**O que ainda não atende (próximas etapas)**

- Volume de ~70 folhas e equilíbrio de ~15 páginas por capítulo.
- Revisão bibliográfica dos últimos cinco anos (Scopus / Connected Papers).
- Capítulos de Resultados e Conclusão no tom “vender o peixe” (o Resumo abaixo já antecipa o que a Conclusão deverá responder).
- Diagnósticos extras de defesa (VIF, validação interna da AUC), se autorizados, sem trocar o modelo principal.

**Como a anotação “análise de 5 variáveis” foi resolvida**

As **13** preditoras permanecem no ajuste (controle de confundimento; conjunto a priori do Cleveland). **Cinco** (`ca`, `sex`, `cp`, `thal`, `thalach`) são as que a narrativa de Resultados deve destacar. As outras oito não saem do modelo; mudam só o peso na interpretação. Ver Tabela 1.

**DFA, DCCA, ROC e Brier**

ROC/AUC e Brier **cabem** e já estão no pipeline. DFA e DCCA **não cabem** como análise deste dataset (amostra transversal, não série temporal). A exclusão fica justificada em texto na seção 3.4 — fundamentação, não método forçado.

---

# ELEMENTOS PRÉ-TEXTUAIS

---

## Capa

```
[INSTITUIÇÃO]
[UNIDADE / CENTRO / FACULDADE]
[PROGRAMA DE PÓS-GRADUAÇÃO]

[NOME COMPLETO DO AUTOR]

ASSOCIAÇÃO ENTRE VARIÁVEIS CLÍNICAS E PRESENÇA DE
DOENÇA CARDÍACA: ANÁLISE BIVARIADA E REGRESSÃO
LOGÍSTICA NO SUBCONJUNTO CLEVELAND (UCI)

[CIDADE]
[ANO]
```

---

## Folha de rosto

```
[NOME COMPLETO DO AUTOR]

ASSOCIAÇÃO ENTRE VARIÁVEIS CLÍNICAS E PRESENÇA DE
DOENÇA CARDÍACA: ANÁLISE BIVARIADA E REGRESSÃO
LOGÍSTICA NO SUBCONJUNTO CLEVELAND (UCI)

Dissertação apresentada ao [PROGRAMA DE PÓS-GRADUAÇÃO]
da [INSTITUIÇÃO] como requisito parcial para obtenção do
título de Mestre em [NOME DO CURSO / ÁREA DE CONCENTRAÇÃO].

Orientador(a): [NOME COMPLETO DO(A) ORIENTADOR(A)]
Coorientador(a): [NOME, SE HOUVER; CASO NÃO HAJA, OMITIR ESTA LINHA]

[CIDADE]
[ANO]
```

Ficha catalográfica: a gerar pela biblioteca da instituição (não inventar número de classificação).

---

## Folha de aprovação

```
[NOME COMPLETO DO AUTOR]

ASSOCIAÇÃO ENTRE VARIÁVEIS CLÍNICAS E PRESENÇA DE
DOENÇA CARDÍACA: ANÁLISE BIVARIADA E REGRESSÃO
LOGÍSTICA NO SUBCONJUNTO CLEVELAND (UCI)

Dissertação apresentada ao [PROGRAMA] da [INSTITUIÇÃO]
como requisito parcial para obtenção do título de Mestre
em [ÁREA].

Aprovada em: ____ / ____ / ________

Banca examinadora

Prof(a). Dr(a). [ORIENTADOR(A)] — [INSTITUIÇÃO]
Orientador(a)

Prof(a). Dr(a). [EXAMINADOR INTERNO] — [INSTITUIÇÃO]
Examinador(a)

Prof(a). Dr(a). [EXAMINADOR EXTERNO] — [INSTITUIÇÃO]
Examinador(a)

_________________________________
Assinatura do(a) orientador(a)

_________________________________
Assinatura do(a) examinador(a) interno(a)

_________________________________
Assinatura do(a) examinador(a) externo(a)
```

---

## Dedicatória

[PREENCHER — texto breve, opcional. Não inventar nomes de familiares.]

---

## Agradecimentos

[PREENCHER — orientador(a), banca, instituição, eventuais agências de fomento. Não inventar financiamento nem pessoas.]

---

## Epígrafe

[PREENCHER — citação opcional, com autoria e fonte. Deixar em branco se não houver escolha.]

---

## Resumo

Este trabalho identificou associações entre variáveis clínicas e de exame e a presença de doença cardíaca, contrastando a análise bivariada com os efeitos ajustados de um modelo logístico. Utilizaram-se dados secundários, públicos e anonimizados do repositório UCI Machine Learning Repository, subconjunto Cleveland (14 atributos clássicos e diagnóstico angiográfico). Após recodificação para os códigos numéricos da documentação UCI e exclusão de valores em falta em `ca`, `thal` e `slope`, a amostra analítica compreendeu 297 observações (160 sem doença angiográfica significativa e 137 com doença). Esperava-se (i) rejeitar a hipótese nula global de ausência de associação após o ajuste simultâneo pelas 13 preditoras e (ii) observar que parte das associações brutas não se sustentaria no modelo multivariado, evidenciando confundimento. A bivariada empregou correlação de Spearman (contínuas e `ca`), teste qui-quadrado (categóricas) e odds ratio bruto para o sexo. A multivariada foi uma regressão logística binária com intercepto; a discriminação foi avaliada pela curva ROC (AUC) e o erro quadrático das probabilidades pelo Brier score, comparado ao modelo nulo de prevalência constante. O teste de razão de verossimilhança rejeitou a hipótese nula global (p = 1,14 × 10⁻³⁶; pseudo-R² de McFadden = 0,50). Mantiveram associação independente, entre outras, `ca`, `sex`, `cp`, `thal` e `thalach` (esta última com sinal negativo, coerente com a anti-correlação de Spearman). Idade, colesterol e `oldpeak` associaram-se na bivariada e perderam significância após o ajuste. A AUC in-sample foi 0,925 e o Brier do modelo (0,107) foi inferior ao do nulo (0,249); ambos tendem a ser otimistas por terem sido calculados na amostra do ajuste. Conclui-se, no recorte metodológico adotado, que a logística binária com avaliação ROC/Brier foi adequada ao desfecho dicotômico e à pergunta de associação bruta versus independente. Técnicas de flutuação destendenciada (DFA/DCCA) não se aplicam a esta amostra transversal.

**Palavras-chave:** doença cardíaca; regressão logística; correlação de Spearman; curva ROC; Brier score; dados secundários; UCI Cleveland.

---

## Abstract

This study identified associations between clinical and examination variables and the presence of heart disease, contrasting bivariate analysis with adjusted effects from a logistic model. It used secondary, public, anonymized data from the UCI Machine Learning Repository, Cleveland subset (14 classic attributes and angiographic diagnosis). After recoding to the numeric codes in the UCI documentation and excluding missing values in `ca`, `thal`, and `slope`, the analytic sample comprised 297 observations (160 without significant angiographic disease and 137 with disease). The expected findings were (i) rejection of the global null hypothesis of no association after simultaneous adjustment for the 13 predictors and (ii) that some crude associations would not hold in the multivariable model, indicating confounding. The bivariate stage used Spearman correlation (continuous variables and `ca`), the chi-square test (categorical variables), and a crude odds ratio for sex. The multivariable stage was a binary logistic regression with an intercept; discrimination was assessed with the ROC curve (AUC) and the mean squared error of predicted probabilities with the Brier score, compared with a null model of constant prevalence. The likelihood-ratio test rejected the global null (p = 1.14 × 10⁻³⁶; McFadden’s pseudo-R² = 0.50). Independent associations remained for, among others, `ca`, `sex`, `cp`, `thal`, and `thalach` (the last with a negative sign, consistent with the Spearman anticorrelation). Age, cholesterol, and `oldpeak` were associated in the bivariate analysis and lost significance after adjustment. The in-sample AUC was 0.925 and the model Brier score (0.107) was lower than that of the null (0.249); both tend to be optimistic because they were computed on the fitting sample. Within the adopted methodological scope, binary logistic regression with ROC/Brier evaluation was appropriate for a dichotomous outcome and for the question of crude versus independent association. Detrended fluctuation methods (DFA/DCCA) do not apply to this cross-sectional sample.

**Keywords:** heart disease; logistic regression; Spearman correlation; ROC curve; Brier score; secondary data; UCI Cleveland.

---

## Lista de ilustrações

| Figura | Título (provisório) | Capítulo previsto |
| --- | --- | --- |
| Figura 1 | Curva ROC do modelo logístico (amostra completa, in-sample) | 4 |

Outras figuras (fluxograma da amostra, gráfico de calibração) só entram nesta lista se forem de fato produzidas nos capítulos.

---

## Lista de tabelas

| Tabela | Título | Onde está neste rascunho / destino |
| --- | --- | --- |
| Tabela 1 | Preditoras no modelo (13) versus ênfase narrativa (5) | Capítulo 3 |
| Tabela 2 | Características da amostra (N = 297) | Capítulo 4 |
| Tabela 3 | Correlação de Spearman com o desfecho | Capítulo 4 |
| Tabela 4 | Teste qui-quadrado de independência | Capítulo 4 |
| Tabela 5 | Contingência sexo × desfecho e odds ratio bruto | Capítulo 4 |
| Tabela 6 | Regressão logística: coeficientes, OR ajustados e IC95% | Capítulo 4 |
| Tabela 7 | Desempenho discriminativo (AUC e Brier, in-sample) | Capítulo 4 |

Os critérios de uso e de exclusão das técnicas **não** entram como tabela: ficam em texto corrido na seção 3.4. A numeração das Tabelas 2–7 será conferida na diagramação.

---

## Lista de abreviaturas e siglas

| Sigla | Significado |
| --- | --- |
| AUC | Área sob a curva ROC (*Area Under the Curve*) |
| DCCA | Análise de correlação cruzada destendenciada (*Detrended Cross-Correlation Analysis*) |
| DFA | Análise de flutuação destendenciada (*Detrended Fluctuation Analysis*) |
| DP | Desvio padrão |
| EPV | Eventos por variável (*events per variable*) |
| H0 | Hipótese nula |
| H1 | Hipótese alternativa |
| IC95% | Intervalo de confiança de 95% |
| LR | Teste de razão de verossimilhança (*likelihood-ratio*) |
| ML | Aprendizado de máquina (*machine learning*) |
| N | Tamanho amostral |
| OR | *Odds ratio* (razão de chances) |
| ROC | *Receiver Operating Characteristic* |
| UCI | *University of California, Irvine* (repositório de aprendizado de máquina) |
| VIF | Fator de inflação da variância (*Variance Inflation Factor*) |

---

## Sumário

(Paginação indicativa para o alvo de ~70 folhas, com capítulos de cerca de 15 páginas. Os números serão atualizados na diagramação final.)

```
1  INTRODUÇÃO                                              ~15 p.
   1.1 Contextualização e problema de pesquisa
   1.2 Objetivos (geral e específicos)
   1.3 Hipóteses
   1.4 Justificativa e contribuições
   1.5 Organização da dissertação

2  FUNDAMENTAÇÃO TEÓRICA E REVISÃO DA LITERATURA           ~15 p.
   2.1 Doença cardíaca e o desfecho angiográfico
   2.2 Associação bruta, confundimento e efeito ajustado
   2.3 Regressão logística, OR e testes de hipóteses
   2.4 Spearman, qui-quadrado e medidas de desempenho (ROC, Brier)
   2.5 Revisão recente (Scopus / Connected Papers, últimos 5 anos)
   2.6 Lacuna e posicionamento deste trabalho

3  METODOLOGIA                                             ~15 p.
   3.1 Tipo de estudo e natureza dos dados
   3.2 Fonte, recorte Cleveland e pré-processamento
   3.3 Variáveis e codificação UCI
   3.4 Critérios de escolha das técnicas (texto)
   3.5 Critérios das 13 preditoras e das 5 em destaque (Tabela 1)
   3.6 Análise descritiva e bivariada
   3.7 Modelo logístico e hipóteses
   3.8 Avaliação do modelo (ROC/AUC e Brier)
   3.9 Aspectos éticos (dados secundários anonimizados)
   3.10 Limitações metodológicas previstas

4  RESULTADOS E DISCUSSÃO                                  ~15 p.
   4.1 O que foi feito e como foi feito (protocolo executado)
   4.2 O que se esperava encontrar
   4.3 Caracterização da amostra
   4.4 Associações bivariadas
   4.5 Modelo ajustado e contraste bruto versus independente
   4.6 Ênfase interpretativa nas cinco variáveis destacadas
   4.7 Desempenho (ROC e Brier) e leitura cautelosa (in-sample)
   4.8 Discussão à luz da literatura e da lógica clínica da codificação UCI

5  CONCLUSÃO                                               ~6–8 p.

REFERÊNCIAS                                                ~4–6 p.
APÊNDICE A — Tabelas numéricas geradas pelo código
APÊNDICE B — Figura da curva ROC
```

**Pré-textuais + pós-textuais:** cerca de 10 a 12 folhas no conjunto, de modo que o volume total se aproxime de 70.

Os Capítulos 1 a 5, as Referências e os Apêndices estão em `capitulos_dissertacao.md`. A seção seguinte antecipa o material da Metodologia (critérios em texto + Tabela 1 das variáveis).

---

# MATERIAL PARA O CAPÍTULO 3 (antecipado)

## Critérios gerais de escolha das técnicas

A seleção metodológica obedeceu a cinco critérios, aplicados antes da interpretação dos p-valores:

1. **Tipo de desfecho.** O diagnóstico foi dicotomizado (`target` 0/1). Técnicas para resposta contínua, tempo até o evento ou trajetória temporal ficam excluídas.
2. **Tipo de preditora.** Contínuas e a contagem ordinal `ca` pedem associação monotônica; categóricas pedem teste de contingência.
3. **Pergunta científica.** O objeto é **associação** (sinal, magnitude, persistência após ajuste), não apenas acurácia preditiva nem causalidade.
4. **Desenho dos dados.** Uma linha por paciente, sem eixo temporal. Métodos de séries (DFA, DCCA) não se aplicam.
5. **Alinhamento com o protocolo da dissertação.** Bivariada clássica seguida de logística e de avaliação probabilística (ROC e Brier), sem substituir o núcleo por seleção automática ou por aprendizado de máquina.

A seção 3.4 justifica em texto, e não em tabela, cada técnica usada e cada técnica recusada. A Tabela 1 (abaixo) separa apenas **inclusão no modelo** (13 variáveis) de **ênfase na narrativa** (5 variáveis). O texto definitivo da 3.4 está em `capitulos_dissertacao.md`.

Em resumo: usaram-se logística (desfecho 0/1 e OR ajustado), Spearman (monotônico, admite anti-correlação), qui-quadrado (categóricas), OR bruto de sexo (contraste com o ajustado), ROC/AUC (discriminação) e Brier versus nulo (erro quadrático das probabilidades; cabe e não concorre com a ROC). Não se usaram DFA nem DCCA (exigem série temporal; o Cleveland é transversal), Pearson como método principal, MQO, Cox, *stepwise*/Logit só com 5 preditoras, nem ML no núcleo. DFA e DCCA não devem ser forçadas para aumentar o número de páginas; o espaço vai para a justificativa do desenho, a revisão Scopus e o contraste bruto versus ajustado.

---

## Tabela 1. As 13 preditoras no modelo e as 5 em destaque na narrativa

**Regra.** Todas as linhas com “Sim” em “No modelo?” entram simultaneamente no Logit. “Destaque na narrativa?” = sim apenas para as cinco que o Resultados deve vender com mais detalhe (sinal, OR, coerência clínica da codificação UCI e contraste com a bivariada).

| Variável | Significado (UCI) | No modelo? | Destaque na narrativa? | Critério |
| --- | --- | --- | --- | --- |
| `ca` | Número de vasos principais corados (0–3) | Sim | **Sim** | Maior associação ajustada (β ≈ 1,27; p &lt; 0,001). Spearman ρ = 0,49. Ênfase clínica e estatística. |
| `sex` | 0 feminino; 1 masculino | Sim | **Sim** | Hipótese específica do projeto. OR bruto ≈ 3,57; permanece no ajuste (p = 0,007). |
| `cp` | Tipo de dor torácica (1–4; 4 = assintomático) | Sim | **Sim** | Forte na bivariada (χ²) e no Logit (p = 0,003). Exige explicar a codificação: no Cleveland, o código 4 não é “dor mais leve”. |
| `thal` | Teste de esforço com tálio (3 / 6 / 7) | Sim | **Sim** | Associação independente (p = 0,001). Variável de exame, não só demográfica. |
| `thalach` | Frequência cardíaca máxima atingida | Sim | **Sim** | Anti-correlação (Spearman ρ = −0,43; β &lt; 0 no Logit, p = 0,043). Mostra que o trabalho não busca só correlações positivas. |
| `age` | Idade em anos | Sim | Não | Entra para ajuste. Associa-se na bivariada (ρ = 0,24) e **perde** significância no Logit (p = 0,555): exemplo central de confundimento. |
| `trestbps` | Pressão arterial de repouso | Sim | Não | Permanece no ajuste (p = 0,025), mas o ganho narrativo é menor que o das cinco. Fica no texto da tabela completa de OR. |
| `chol` | Colesterol sérico | Sim | Não | Bivariada limítrofe (ρ = 0,12; p = 0,046); não se sustenta no ajuste (p = 0,186). Serve ao contraste, não à ênfase. |
| `fbs` | Glicemia de jejum &gt; 120 mg/dL | Sim | Não | Qui-quadrado nulo (p = 1). No Logit, p = 0,066 (limítrofe). Não forçar interpretação. |
| `restecg` | Eletrocardiograma de repouso | Sim | Não | Associação bivariada (p = 0,008); não se mantém no ajuste (p = 0,185). |
| `exang` | Angina induzida pelo esforço | Sim | Não | Significativa no Logit (p = 0,025). Fica no modelo e na tabela de OR; a narrativa privilegiou `thalach` como representante do teste ergométrico. |
| `oldpeak` | Depressão de ST induzida pelo esforço | Sim | Não | Spearman forte (ρ = 0,41) e **não** significativa após ajuste (p = 0,243). Melhor exemplo, com a idade, do “caiu no multivariado”. |
| `slope` | Inclinação do segmento ST no pico do esforço | Sim | Não | Qui-quadrado significativo; Logit p = 0,116. Correlacionada conceitualmente com `oldpeak`; permanece para ajuste, sem ênfase. |

### Por que não reduzir o Logit às cinco

- **Confundimento.** Idade, `oldpeak`, `chol` e outras só revelam seu papel (ou a perda de papel) se estiverem **dentro** do modelo. Tirá-las anteciparia o resultado.
- **Protocolo a priori.** As 13 são o conjunto clássico do Cleveland de 14 atributos, não um subconjunto escolhido depois de ver os p-valores.
- **EPV.** Com 137 eventos, 13 preditoras dão cerca de 10,5 eventos por variável (limiar clássico ≈ 10). Um modelo de cinco melhoraria o EPV, mas ao custo de viés por omissão se as excluídas forem confundidoras.
- **Pedido do orientador.** A “análise de cinco variáveis” é atendida na **interpretação** (Tabela 1), não na exclusão das demais.

### Por que estas cinco, e não `exang` ou `trestbps`

`exang` e `trestbps` são significativas no ajuste e **não foram excluídas**. A escolha das cinco privilegia: (1) a maior magnitude (`ca`); (2) a hipótese declarada (`sex`); (3) a variável que mais exige cuidado de codificação (`cp`); (4) um exame complementar (`thal`); (5) o caso explícito de anti-correlação (`thalach`). Duas outras significativas no Logit cabem na tabela de resultados sem receber a mesma extensão de parágrafo.

---

## Encaminhamento (próxima etapa, fora deste ficheiro)

1. Preencher capa, folha de rosto, dedicatória, agradecimentos e nomes da banca.
2. Redigir o Capítulo 2 com literatura **2011–2026** filtrada no Scopus ou no Connected Papers (priorizar os últimos cinco anos na discussão; clássicos metodológicos podem ficar como fundamento).
3. Mover as Tabelas 1 e 2 para o Capítulo 3 e escrever Resultados/Conclusão no roteiro do Resumo: o que fez, como fez, o que esperava, se encontrou, se o método foi o indicado.
4. Se autorizado: acrescentar no código VIF e AUC/Brier em validação cruzada, **sem** trocar o modelo de 13 preditoras.
