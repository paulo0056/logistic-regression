# Capítulos da dissertação (colar no Word)

**Como colar:** no Word, aplicar estilo *Título 1* aos capítulos (`1 INTRODUÇÃO`, `2 FUNDAMENTAÇÃO…`) e *Título 2* às seções (`1.1`, `1.2`…). Corpo: Times New Roman 12, espaçamento 1,5, margens ABNT. Atualizar o sumário automático depois. A Tabela 1 (variáveis no modelo versus ênfase) pode ser convertida para tabela do Word. Inserir no Apêndice B a figura da curva ROC gerada na análise.

**Este ficheiro não contém** capa, resumo nem listas (estão nos elementos pré-textuais).

---

# 1 INTRODUÇÃO

Este capítulo situa o trabalho no campo da modelagem estatística aplicada à saúde cardiovascular, delimita o uso de dados secundários do subconjunto Cleveland e formula o problema de pesquisa em termos de associação — e não de causalidade ou de ranking de algoritmos. As seções seguintes apresentam, nesta ordem, o contexto e a pergunta (1.1), os objetivos (1.2), as hipóteses (1.3), a justificativa (1.4) e o mapa dos demais capítulos (1.5). Nenhuma dessas seções é ornamental: cada uma antecipa o que os Capítulos 3 e 4 executam e o que o Capítulo 5 deve responder.

## 1.1 Contextualização e problema de pesquisa

As doenças do aparelho circulatório permanecem entre as principais causas de morbimortalidade no mundo contemporâneo. Relatórios da Organização Mundial da Saúde reiteram o peso da doença isquêmica do coração e das síndromes correlatas sobre os sistemas de saúde, com ênfase na identificação precoce de indivíduos com maior probabilidade de acometimento (ORGANIZAÇÃO MUNDIAL DA SAÚDE, 2021). No Brasil, o mesmo padrão epidemiológico justifica o interesse acadêmico por métodos que organizem evidência clínica de forma transparente, ainda quando os dados não provenham de coleta primária local.

A modelagem estatística aplicada à saúde não se reduz a classificar pacientes como “doentes” ou “não doentes”. Em dissertações de natureza metodológica, o objeto frequentemente é outro: **medir associação**, distinguir o que aparece na análise bruta do que permanece depois do ajuste simultâneo por covariáveis, e comunicar incerteza. Essa distinção importa porque variáveis correlacionadas entre si — idade, capacidade de esforço, alterações eletrocardiográficas, sexo — podem produzir associações espúrias ou infladas quando examinadas isoladamente (VANDERWEELE, 2019; HOSMER; LEMESHOW; STURDIVANT, 2013).

O presente trabalho opera sobre um recorte clássico da literatura de aprendizado de máquina e de estatística aplicada: o conjunto *Heart Disease* do repositório UCI Machine Learning Repository, subconjunto **Cleveland**, com os 14 atributos habitualmente publicados (JÁNOSI et al., 1989; DETRANO et al., 1989). São **dados secundários, públicos e anonimizados**. Não houve coleta clínica pelo autor, nem acesso a identificadores de pacientes. Na redação acadêmica, “dados didáticos” ou “não primários” não devem ser lidos como “dados fabricados”: o Cleveland é um dataset histórico real, amplamente reutilizado em ensino e em pesquisa metodológica.

Após recodificação para os códigos numéricos da documentação UCI e exclusão de valores em falta nas variáveis `ca`, `thal` e `slope`, a amostra analítica compreende **297 observações**, com desfecho binário derivado do campo angiográfico `num`: ausência de doença significativa (`num = 0`, estenose inferior a 50%) versus presença (`num ≥ 1`).

A pergunta que organiza a dissertação é deliberadamente associativa, e não causal nem puramente preditiva:

**Quais variáveis clínicas e de exame se associam à presença de doença cardíaca na análise bivariada, e quais mantêm associação independente após o ajuste simultâneo pelas demais no modelo logístico?**

O interesse recai sobre o **sinal** e a **força** da relação com o desfecho. Correlação positiva e anti-correlação (Spearman negativo; coeficiente logístico negativo) são igualmente informativas. O contraste entre o efeito bruto e o efeito ajustado é o achado substantivo esperado, e não um inconveniente a ser omitido.

## 1.2 Objetivos

Os objetivos traduzem a pergunta da seção 1.1 em tarefas verificáveis. O objetivo geral define o objeto (associação com o desfecho binário) e o recorte (Cleveland). Os específicos seguem a ordem do pipeline: descrever, medir associação bruta, estimar efeitos ajustados, avaliar o modelo e justificar as escolhas metodológicas — inclusive as técnicas que **não** foram usadas. Essa última tarefa atende à orientação de explicitar critérios, e não apenas listar o que o software calculou.

**Objetivo geral.** Identificar e analisar fatores associados à presença de doença cardíaca, no subconjunto Cleveland, por meio de métodos bivariados e de regressão logística binária, com avaliação do desempenho probabilístico do modelo.

**Objetivos específicos.**

a) Caracterizar a amostra analítica (N = 297) quanto ao desfecho e às preditoras contínuas e categóricas.

b) Estimar associações bivariadas com o desfecho: correlação de Spearman para variáveis contínuas e para `ca`; teste qui-quadrado de independência para categóricas; *odds ratio* (OR) bruto no exemplo sexo × desfecho.

c) Estimar efeitos ajustados por regressão logística binária com as 13 preditoras clássicas e intercepto, reportando coeficientes, p-valores e a lógica de OR = exp(β).

d) Avaliar a discriminação (curva ROC e AUC) e o erro quadrático das probabilidades (Brier score), em comparação com um modelo nulo de prevalência constante.

e) Explicitar os critérios de escolha das técnicas (incluindo as não utilizadas, como DFA e DCCA) e distinguir as 13 variáveis do ajuste das cinco privilegiadas na interpretação.

Os itens (a) a (d) materializam-se nos Capítulos 3 e 4. O item (e) materializa-se na seção 3.4 (técnicas) e na Tabela 1 (variáveis). A Conclusão retoma o conjunto para dizer se o que se pretendia medir foi, de fato, medido.

## 1.3 Hipóteses

As hipóteses referem-se ao modelo logístico com as 13 preditoras incluídas simultaneamente. A análise bivariada descreve associações brutas; o teste formal das hipóteses recai sobre os coeficientes ajustados. “Ajuste”, aqui, é essa inclusão conjunta: cada coeficiente se interpreta como associação com o desfecho **mantidas as demais variáveis fixas** (HOSMER; LEMESHOW; STURDIVANT, 2013; SCHOBER; VETTER, 2021). Os objetivos (seção 1.2) indicam o que se calcula; as hipóteses, o que se espera decidir nesse modelo.

**Hipótese nula global (H0).** Após o ajuste pelas 13 covariáveis, não há associação entre o conjunto de preditoras e a probabilidade de doença cardíaca, o que equivale a todos os coeficientes (exceto o intercepto) iguais a zero. O teste de razão de verossimilhança do modelo versus o modelo nulo (somente intercepto) operacionaliza essa hipótese.

**Hipótese alternativa global (H1).** Após o ajuste, pelo menos uma variável permanece associada independentemente ao desfecho (pelo menos um coeficiente diferente de zero).

**Hipótese específica.** O sexo masculino permanece associado a maior *odds* de doença após o controle pelas demais preditoras (teste do coeficiente de `sex`).

Hipóteses pontuais para cada uma das treze variáveis não foram pré-especificadas como bateria de testes confirmatórios, a fim de não converter o trabalho em caça a p-valores. A ênfase narrativa em cinco preditoras (`ca`, `sex`, `cp`, `thal`, `thalach`) é interpretativa e justifica-se no Capítulo 3; **não** equivale a reduzir o Logit a um submodelo de cinco termos.

## 1.4 Justificativa e contribuições

A justificativa explica por que este recorte merece um mestrado, mesmo sem coleta primária e mesmo com um banco já clássico. Três razões sustentam a escolha.

Primeiro, o Cleveland de 14 atributos é um padrão de fato na literatura de classificação, mas uma fração crescente dos artigos recentes o trata sobretudo como banco para comparar acurácia de algoritmos (florestas, SVM, redes), com menor ênfase no contraste entre associação bruta e ajustada (AMZAD HOSSEN et al., 2021). Há espaço para um protocolo explícito de estatística aplicada: Spearman e qui-quadrado na bivariada; logística no ajuste; ROC e Brier no desempenho.

Segundo, a dissertação precisa ser **defendível**. Dados secundários, amostra histórica norte-americana e métricas calculadas na amostra do ajuste (in-sample) são limitações reais. Declará-las na Introdução, e não apenas no final, reduz a assimetria entre o que o texto promete e o que a banca perguntará.

Terceiro, a contribuição esperada não é um escore clínico para o Sistema Único de Saúde. É um **protocolo reprodutível** (código em Python, tabelas exportáveis, figura ROC) que demonstra: (i) como recodificar o export UCI; (ii) como o confundimento aparece empiricamente (variáveis significativas na bivariada que perdem significância no Logit); (iii) por que técnicas de séries temporais (DFA, DCCA) não se aplicam a um corte transversal; (iv) por que o Brier complementa a ROC.

## 1.5 Organização da dissertação

A dissertação está organizada em cinco capítulos de conteúdo, seguidos das referências e de dois apêndices, de modo a equilibrar o volume (cerca de quinze páginas nos Capítulos 1 a 4 e seis a oito na Conclusão, após a diagramação no Word).

O Capítulo 2 constrói o vocabulário teórico: o desfecho angiográfico, a diferença entre associação bruta e ajustada, a logística, as medidas bivariadas e de desempenho (incluindo a pertinência do Brier) e a revisão recente, até posicionar a lacuna. O Capítulo 3 transforma essa fundamentação em procedimentos — fonte, recodificação, critérios das técnicas (seção 3.4) e das variáveis (Tabela 1), modelo e ética. O Capítulo 4 “vende o peixe”: o que foi feito, o que se esperava e o que os números mostraram, com ênfase nas cinco variáveis destacadas e com a ressalva in-sample. O Capítulo 5 responde ao Resumo, ponto a ponto. Os apêndices concentram tabelas numéricas e a figura ROC, para não interromper a argumentação do corpo.

Essa ordem evita antecipar resultados na Introdução e evita repetir, na Conclusão, tabelas que já pertencem ao Capítulo 4. Cada capítulo abre com um parágrafo de encadeamento, precisamente para que nenhum título fique sem texto.

---

# 2 FUNDAMENTAÇÃO TEÓRICA E REVISÃO DA LITERATURA

Este capítulo fornece o aparato conceitual sem o qual os números do Capítulo 4 não se interpretam. A seção 2.1 esclarece o que o Cleveland chama de doença (campo angiográfico `num` e sua dicotomização). A seção 2.2 distingue associação bruta, confundimento e efeito ajustado — o contraste que a dissertação se propõe a mostrar. A seção 2.3 apresenta a logística, o OR e os testes que operacionalizam as hipóteses. A seção 2.4 justifica Spearman, qui-quadrado, ROC/AUC e Brier, e explica por que DFA e DCCA ficam de fora. A seção 2.5 revê literatura recente (com conferência pendente no Scopus institucional). A seção 2.6 formula a lacuna e o posicionamento.

## 2.1 Doença cardíaca e o desfecho angiográfico

Antes de falar em associação, é preciso dizer **o que** se está associando: neste banco, “doença cardíaca” não é um autorrelato nem um código de óbito, e sim um critério angiográfico documentado no campo `num`.

No conjunto Cleveland, o campo original `num` registra o resultado da cineangiocoronariografia em escala ordinal (0 a 4), em que 0 indica ausência de estenose igual ou superior a 50% em vasos principais e valores positivos indicam doença em graus crescentes (DETRANO et al., 1989; JÁNOSI et al., 1989). A tradição analítica do repositório — e a adotada aqui — **dicotomiza** esse campo: `target = 0` se `num = 0`; `target = 1` se `num ≥ 1`.

Essa dicotomização tem custo e benefício. O benefício é alinhar o desfecho a uma regressão logística binária e à pergunta de presença versus ausência. O custo é perder a gradação de gravidade. Modelos ordinais ou politômicos responderiam outra pergunta e exigiriam mais eventos por categoria; não foram o objeto deste mestrado.

As preditoras clássicas misturam demografia (`age`, `sex`), sintomas (`cp`, `exang`), sinais vitais e laboratório (`trestbps`, `chol`, `fbs`), eletrocardiografia de repouso (`restecg`) e de esforço (`thalach`, `oldpeak`, `slope`), anatomia coronariana por contagem de vasos corados (`ca`) e cintilografia com tálio (`thal`). A coexistência de variáveis de exame invasivo ou semi-invasivo com o próprio desfecho angiográfico impõe cautela interpretativa: `ca` está conceitualmente próxima do critério de doença. Isso não impede o uso estatístico no protocolo clássico de 14 atributos; impede tratar o modelo como “triagem ambulatorial com dados de consultório apenas”.

## 2.2 Associação bruta, confundimento e efeito ajustado

Esta seção é o coração teórico do contraste que o Capítulo 4 vai mostrar empiricamente. Sem distinguir efeito bruto e efeito ajustado, qualquer p-valor da bivariada seria tratado, por engano, como resposta final.

Associação bruta é a que se observa entre uma exposição (ou preditora) e o desfecho **sem** controlar outras variáveis. Pode ser expressa por diferença de médias, Spearman, qui-quadrado ou OR de tabela 2×2. Associação ajustada é a que resta quando outras covariáveis estão no modelo (VANDERWEELE, 2019).

Confundimento, em linguagem operacional suficiente para esta dissertação, ocorre quando uma terceira variável se associa tanto à preditora de interesse quanto ao desfecho e distorce a associação bruta. Idade, por exemplo, correlaciona-se com frequência máxima no esforço e com a prevalência de doença coronariana; uma associação bruta de `thalach` com o desfecho mistura capacidade funcional e estrutura etária da amostra. O Logit com as 13 preditoras não “prova causalidade”; ele estima associações **condicionais** à especificação adotada.

O OR bruto do sexo ilustra a pedagogia do contraste: um único número resume a tabela 2×2. O OR ajustado de `sex` responde se a diferença entre homens e mulheres permanece depois de considerar dor, exames e demais covariáveis. Se os dois ORs divergem, há evidência descritiva de confundimento ou de mediação mal separada — o texto não pretende identificar o mecanismo causal, apenas registrar o contraste.

Manter as 13 variáveis no ajuste, em vez de pré-selecionar cinco, é coerente com essa lógica: variáveis que “caem” no multivariado só revelam esse papel se estiverem no modelo (HOSMER; LEMESHOW; STURDIVANT, 2013).

## 2.3 Regressão logística, OR e testes de hipóteses

A logística é o modelo da pergunta central: desfecho 0/1 e interesse em razões de chances ajustadas (HOSMER; LEMESHOW; STURDIVANT, 2013; PENG; LEE; INGERSOLL, 2002; SCHOBER; VETTER, 2021). A notação abaixo é a que o Capítulo 3 estima e o Capítulo 4 reporta.

Seja π a probabilidade de `target = 1`. O modelo logístico especifica

logit(π) = ln[π / (1 − π)] = β₀ + β₁x₁ + … + βₖxₖ.

O coeficiente βⱼ é a variação do logito associada ao aumento de uma unidade em xⱼ, mantidas as demais fixas. A exponencial exp(βⱼ) é o OR ajustado correspondente (HOSMER; LEMESHOW; STURDIVANT, 2013; SCHOBER; VETTER, 2021). Intervalos de confiança de 95% para o OR obtêm-se exponenciando os limites do IC do coeficiente.

A estimação é por máxima verossimilhança. O teste de razão de verossimilhança compara o logaritmo da verossimilhança do modelo completo com o do modelo nulo (somente intercepto). Um p-valor pequeno rejeita a H0 global de que todos os βⱼ (j ≥ 1) são nulos. O pseudo-R² de McFadden, 1 − (ℓ_modelo / ℓ_nulo), resume o ganho relativo de verossimilhança; valores da ordem de 0,2 a 0,4 já são frequentemente considerados notáveis em ciências sociais e da saúde, e valores próximos de 0,5 indicam ajuste descritivo substancial **na amostra**, sem garantir generalização.

A regra empírica de cerca de **dez eventos por variável** (EPV) em logística (PEDUZZI et al., 1996) é um aviso de estabilidade, não um teorema. Com 137 eventos e 13 preditoras, o EPV deste trabalho situa-se próximo de 10,5: aceitável para um mestrado metodológico, folgado o suficiente para não inflar o modelo com interações e termos polinomiais sem plano prévio.

Schober e Vetter (2021) enfatizam o uso da logística na pesquisa médica precisamente quando o desfecho é binário e se deseja comunicar razões de chances. Essa é a justificativa teórica para não substituir o núcleo da dissertação por algoritmos cuja saída principal é acurácia.

## 2.4 Spearman, qui-quadrado e medidas de desempenho (ROC, Brier)

A bivariada e a avaliação do modelo não são apêndices da logística: cada técnica responde a uma pergunta distinta. Spearman e qui-quadrado descrevem associação sem ajuste; ROC e Brier descrevem o comportamento das probabilidades depois do ajuste. DFA e DCCA entram só para deixar explícito o que **não** se aplica a este desenho.

**Spearman.** O coeficiente ρ de Spearman mede associação monotônica a partir de postos (SPEARMAN, 1904). Com desfecho binário, interpreta-se como tendência de a preditora ordenar-se com a presença da doença. Aceita sinal negativo (anti-correlação). É preferível a Pearson neste protocolo porque não exige linearidade na escala original e acomoda `ca` como contagem ordinal 0–3.

**Qui-quadrado de independência.** Para preditoras categóricas, testa se a distribuição conjunta com `target` é compatível com independência. Não informa direção. Células esparsas podem distorcer o teste; o caso de `fbs` neste dataset ilustra associação bruta nula.

**ROC e AUC.** A curva ROC confronta taxa de verdadeiros positivos e de falsos positivos ao variar o limiar sobre a probabilidade predita. A área sob a curva (AUC) é a probabilidade de o modelo atribuir escore maior a um caso doente escolhido ao acaso do que a um não doente (HANLEY; MCNEIL, 1982). AUC = 0,5 equivale ao acaso. A ROC **cabe** neste trabalho: o Logit produz π̂ e o desfecho é 0/1. A ressalva obrigatória é o cálculo **in-sample**, otimista para desempenho em novas amostras (STEYERBERG, 2019).

**Brier score.** Brier (1950) definiu a média dos erros quadráticos entre probabilidade predita e desfecho observado. Valores menores são melhores. A ROC não substitui o Brier: a primeira enfatiza ordenação (discriminação); o segundo penaliza probabilidades afastadas do ocorrido (STEYERBERG, 2019; HOESSLY, 2025). Comparar o Brier do modelo ao Brier de um nulo que prevê a prevalência da amostra evita o número isolado e responde se há ganho frente a “chutar a média”.

Hoessly (2025) alerta contra interpretações ingênuas — por exemplo, tratar Brier = 0 como requisito de modelo perfeito em desfechos binários, ou comparar Brier entre populações com prevalências distintas. Neste trabalho, a comparação é **interna** (modelo versus nulo, mesma amostra), o que respeita esse cuidado. O Brier **cabe** e fortalece a defesa: mostra que a avaliação não se encerra na AUC.

**DFA e DCCA (apenas como contraste).** A análise de flutuação destendenciada (DFA) estima propriedades de escala em séries ou sinais longos (PENG et al., 1994). A análise de correlação cruzada destendenciada (DCCA) estende a ideia a dois processos no tempo (PODOBNIK; STANLEY, 2008; ZEBENDE, 2011). Ambas pressupõem ordenação temporal. O Cleveland é um **corte transversal** (uma linha por paciente). Aplicá-las aqui seria inadequação ao desenho, não sofisticação. A fundamentação dessa exclusão ocupa espaço legítimo na Metodologia (seção 3.4).

## 2.5 Revisão recente (Scopus / Connected Papers, últimos 5 anos)

A orientação do programa pede literatura dos últimos cinco anos, com busca no Scopus ou no Connected Papers. Esta seção cumpre o espírito dessa exigência com fontes públicas identificáveis por DOI. A busca institucional completa — *login* da biblioteca, filtro 2021–2026 e exportação do `.bib` — deve ainda ser refeita pelo autor. Itens cuja paginação ou volume não foram conferidos no PDF oficial recebem a marca `[VERIFICAR NO SCOPUS]`.

No eixo clínico-estatístico, Schober e Vetter (2021) reafirmam a logística como ferramenta padrão para desfechos binários em pesquisa médica, com ênfase na interpretação de OR. No eixo de dados Cleveland, Amzad Hossen et al. (2021) comparam floresta aleatória, árvore de decisão e logística sobre os 14 atributos e reportam acurácia elevada para a logística (cerca de 92% na configuração dos autores). O artigo é típico da vaga recente: o objetivo declarado é **prever** a doença, não decompor associação bruta versus ajustada.

Trabalhos posteriores reiteram o Cleveland como banco de comparação entre logística, SVM e vizinhos mais próximos, ou entre modelos lineares interpretáveis (GLM, Lasso, LDA), quase sempre com métricas de classificação em divisão treino-teste `[VERIFICAR NO SCOPUS]`. A linha é complementar à desta dissertação: mostra que a logística permanece competitiva em acurácia, mas raramente discute Spearman, qui-quadrado, OR bruto de sexo ou Brier versus nulo.

Na avaliação de modelos, a literatura de 2025–2026 insiste em não julgar predição individual só pela AUC (c-estatística) e em ler o Brier com cautela quanto a prevalência e calibração (HOESSLY, 2025). Isso justifica, no protocolo desta dissertação, reportar **AUC e Brier juntos**, com o nulo de prevalência, e declarar o viés in-sample em vez de omiti-lo.

Em síntese, os últimos cinco anos consolidam três fatos úteis ao posicionamento: (1) doença cardiovascular permanece prioridade de saúde pública (ORGANIZAÇÃO MUNDIAL DA SAÚDE, 2021); (2) o Cleveland continua a ser reanalisado, sobretudo sob a ótica de ML; (3) a combinação logística + ROC + Brier é reconhecida, mas o contraste bivariada/multivariada é menos enfatizado do que rankings de acurácia.

## 2.6 Lacuna e posicionamento deste trabalho

A lacuna não é a inexistência de artigos sobre o Cleveland. O repositório é um dos mais reanalisados da estatística aplicada e do aprendizado de máquina. O que falta, com frequência, é um **protocolo de associação** explícito: bivariada com sinal (incluindo anti-correlação), ajuste logístico com as 13 preditoras a priori, contraste bruto versus independente, ROC e Brier lidos em conjunto, e recusa fundamentada de métodos incompatíveis com o desenho.

Este mestrado posiciona-se, portanto, como estudo metodológico observacional transversal, com dados secundários. Recodifica o export textual para códigos UCI, a fim de não misturar legendas em inglês com a documentação clássica. Reporta o sinal das associações, inclusive o Spearman negativo de `thalach`. Recusa reduzir o Logit a cinco preditoras escolhidas depois de ver os p-valores; as cinco entram na ênfase interpretativa, não na especificação do modelo. Recusa DFA e DCCA porque o banco não é série temporal. Aceita o Brier como medida pertinente, ao lado da AUC. Limita as pretensões clínicas: não oferece escore para o Brasil e não afirma causalidade.

O Capítulo 3 traduz esse posicionamento em procedimentos replicáveis. O Capítulo 4 verifica se a H0 global cai, se parte das associações brutas se apaga e se sexo e `thalach` se comportam como a fundamentação antecipou.

---

# 3 METODOLOGIA

Este capítulo descreve o desenho, a fonte, as variáveis, os critérios de inclusão e exclusão de técnicas e de ênfase interpretativa, o modelo e os limites éticos e estatísticos do estudo. A ordem das seções replica o pipeline da análise. A seção 3.4 e a Tabela 1 são peças centrais: a primeira justifica, em texto, por que se usou determinada técnica e por que se recusou outra; a segunda registra por que se destacaram cinco variáveis sem tirar as demais do ajuste. Os resultados numéricos ficam no Capítulo 4 e no Apêndice A; aqui importa a **reprodutibilidade** da escolha.

## 3.1 Tipo de estudo e natureza dos dados

Trata-se de estudo **observacional, transversal, com dados secundários**. Observacional, porque não há alocação de intervenção. Transversal, porque cada paciente contribui com um único registro, no momento do exame e da angiografia documentada no banco. Secundário, porque os dados já existiam no repositório UCI; o autor não coletou clínica, não entrevistou pacientes e não acessou prontuários.

A unidade de análise é o indivíduo (uma linha da tabela). Não há seguimento, nem data de eventos repetidos, nem sinal fisiológico contínuo. Essa natureza exclui, de saída, análise de sobrevivência e métodos de séries temporais, o que a seção 3.4 justifica em detalhe. O caráter secundário implica ainda que não se generaliza automaticamente para a população brasileira contemporânea: o estudo ensina um protocolo e estima associações **neste** recorte.

## 3.2 Fonte, recorte Cleveland e pré-processamento

A fonte é o conjunto *Heart Disease* do repositório UCI Machine Learning Repository, recortado ao subconjunto Cleveland e recodificado para os códigos numéricos da documentação original (JÁNOSI et al., 1989). O recorte Cleveland, e não a concatenação com Hungria, Suíça ou Long Beach, segue a tradição do próprio repositório: o subconjunto mais completo e o mais citado nos experimentos publicados.

A coluna de frequência máxima, exportada por vezes como `thalch`, foi renomeada para `thalach`, nome da documentação UCI. Sexo, tipo de dor, eletrocardiograma, declive do ST e tálio, quando textuais, foram mapeados para os códigos numéricos clássicos. Indicadores booleanos (`fbs`, `exang`) foram convertidos para 0/1. O desfecho `target` foi criado a partir de `num ≥ 1`. Observações com falha em `ca`, `thal` ou `slope` foram excluídas (análise de casos completos). A amostra final é N = 297.

Os procedimentos foram implementados em linguagem Python. O código e as tabelas que reproduzem os resultados encontram-se no repositório do autor, para conferência e replicação, e não precisam ser nomeados no corpo do texto.

## 3.3 Variáveis e codificação UCI

Esta seção define o dicionário usado em todo o restante do texto. Sem ele, a banca não tem como julgar o sinal de `cp` ou de `thal`. O desfecho e as treze preditoras são os 14 atributos clássicos, após a criação de `target` e a exclusão de `num`.

**Desfecho.** `target`: 0 = sem doença angiográfica significativa (`num = 0`, estenose inferior a 50%); 1 = com doença (`num ≥ 1`). A dicotomização alinha o problema à logística binária e descarta a gradação 1–4, conforme justificado na seção 2.1.

**Preditoras (13).** `age` (anos); `sex` (0 feminino, 1 masculino); `cp` (1 angina típica, 2 atípica, 3 não anginosa, 4 assintomático); `trestbps` (pressão de repouso, mmHg); `chol` (colesterol, mg/dL); `fbs` (1 se glicemia de jejum > 120 mg/dL); `restecg` (0 normal, 1 anomalia ST-T, 2 hipertrofia ventricular esquerda); `thalach` (frequência máxima atingida); `exang` (1 angina ao esforço); `oldpeak` (depressão de ST); `slope` (1 ascendente, 2 plano, 3 descendente); `ca` (vasos principais corados, 0–3); `thal` (3 normal, 6 defeito fixo, 7 defeito reversível).

Códigos de `cp`, `slope`, `restecg` e `thal` foram tratados como numéricos no Logit, sob o argumento de tendência ordinal, parcimônia e EPV. Essa escolha é discutível: os intervalos entre códigos não são necessariamente iguais, sobretudo em `thal` (3, 6 e 7). Assume-se como limitação metodológica, não como escala intervalar verdadeira. Uma análise de sensibilidade com variáveis dummy pode figurar em trabalho futuro, sem alterar o modelo principal desta dissertação.

## 3.4 Critérios de escolha das técnicas

A escolha das técnicas foi justificada em prosa, e não em quadro-resumo, para que cada decisão apareça com o critério que a sustenta — e não como uma lista de “sim/não”. Os critérios foram fixados **antes** da leitura dos p-valores, para que a especificação não pareça dirigida pelo resultado. Cinco regras governaram inclusão e exclusão: o desfecho é binário; o tipo da preditora (contínua/ordinal versus categórica) define o teste bivariado; a pergunta é de **associação**, não só de acurácia nem de causalidade; o desenho é transversal, o que exclui métodos de séries; e o protocolo da dissertação encadeia bivariada clássica, logística e avaliação probabilística (ROC e Brier).

Adotou-se a **regressão logística binária** como modelo principal porque o desfecho é 0/1 e a pergunta exige efeitos ajustados na escala de *odds*, com teste global da H0 pelo teste de razão de verossimilhança. O modelo produz OR interpretáveis e não exige linearidade da probabilidade, apenas linearidade no *logit* (HOSMER; LEMESHOW; STURDIVANT, 2013; SCHOBER; VETTER, 2021). A **correlação de Spearman** foi usada nas contínuas e em `ca` (contagem 0–3) porque mede associação monotônica, admite anti-correlação e é mais adequada a postos do que Pearson; informa sinal e força brutos, sem substituir o ajuste. O **qui-quadrado de independência** foi o teste das categóricas: detecta dependência em tabelas de contingência, sem impor direção — esta fica a cargo de percentuais, do OR ou do Logit. O **OR bruto de sexo** exemplifica a magnitude 2×2 sem covariáveis, a confrontar com o OR ajustado de `sex`. A **curva ROC e a AUC** avaliam discriminação das probabilidades preditas; cabem ao desfecho binário, com a ressalva de serem in-sample (HANLEY; MCNEIL, 1982). O **Brier score**, comparado ao nulo de prevalência constante, também cabe: é regra própria para probabilidades e mede o erro quadrático que a ROC não captura. Menor Brier é melhor; a comparação com o nulo evita o número isolado (BRIER, 1950; HOESSLY, 2025).

Não se usou **DFA** nem **DCCA**. Ambas exigem série temporal — a primeira, um sinal longo com ordenação no tempo; a segunda, dois processos concomitantes (PENG et al., 1994; PODOBNIK; STANLEY, 2008; ZEBENDE, 2011). O Cleveland é um corte transversal: um registro por paciente, sem eixo temporal. Aplicá-las seria inadequação ao desenho, não sofisticação. Essa exclusão ocupa espaço legítimo na fundamentação, em vez de forçar um gráfico de flutuação para aumentar o volume. Também não se usou **Pearson** como método principal (o desfecho é binário e o interesse é monotônico), nem **regressão linear** (o MQO prevê fora de [0, 1] e não produz OR), nem **Cox** (não há tempo até o evento). Não se reduziu o Logit por *stepwise* nem a cinco preditoras no ajuste: o conjunto de 13 atributos é a priori, o EPV está no limiar clássico e omitir confundidores destruiria o contraste bruto versus ajustado. As cinco variáveis da seção 3.5 são destaque interpretativo, não um submodelo. Por fim, **aprendizado de máquina** (floresta, SVM, redes) ficou de fora do núcleo porque o objeto é associação e OR, não ranking de acurácia; pode figurar como trabalho futuro de predição, separado deste protocolo.

Em síntese, logística, Spearman, qui-quadrado, OR bruto, ROC e Brier formam um encadeamento coerente com o tipo de variável, o desfecho e a pergunta. As técnicas recusadas o foram por incompatibilidade de escala, de desenho ou de objeto — não por desconhecimento.

## 3.5 Critérios das 13 preditoras e das 5 em destaque (Tabela 1)

A anotação de “analisar cinco variáveis” foi atendida na **interpretação**, não na especificação do modelo. Todas as 13 preditoras clássicas entram no Logit. Cinco recebem ênfase na narrativa de Resultados: `ca`, `sex`, `cp`, `thal` e `thalach`. As demais permanecem no ajuste; várias ilustram, justamente, o contraste bruto versus ajustado. A Tabela 1 registra, linha a linha, essa dupla decisão.

**Tabela 1 — Preditoras no modelo (13) versus ênfase narrativa (5)**

| Variável | Significado (UCI) | No modelo? | Destaque na narrativa? | Critério |
| --- | --- | --- | --- | --- |
| `ca` | Vasos principais corados (0–3) | Sim | Sim | Maior associação ajustada; Spearman elevado. |
| `sex` | 0 feminino; 1 masculino | Sim | Sim | Hipótese específica; OR bruto a confrontar com o ajustado. |
| `cp` | Tipo de dor (1–4; 4 = assintomático) | Sim | Sim | Forte na bivariada e no Logit; exige explicar a codificação UCI. |
| `thal` | Cintilografia (3 / 6 / 7) | Sim | Sim | Associação independente; variável de exame. |
| `thalach` | Frequência máxima atingida | Sim | Sim | Anti-correlação (Spearman e β negativos). |
| `age` | Idade | Sim | Não | Ajuste; cai no Logit (confundimento). |
| `trestbps` | Pressão de repouso | Sim | Não | Permanece no ajuste; menor ganho narrativo que as cinco. |
| `chol` | Colesterol | Sim | Não | Bivariada limítrofe; não se sustenta no ajuste. |
| `fbs` | Glicemia de jejum elevada | Sim | Não | Qui-quadrado nulo; Logit limítrofe. |
| `restecg` | ECG de repouso | Sim | Não | Bivariada significativa; perde no ajuste. |
| `exang` | Angina ao esforço | Sim | Não | Significativa no Logit; a narrativa privilegiou `thalach` no bloco ergométrico. |
| `oldpeak` | Depressão de ST | Sim | Não | Spearman forte; perde no ajuste. |
| `slope` | Inclinação do ST | Sim | Não | Qui-quadrado significativo; Logit não significativo. |

A Tabela 1 separa duas decisões que a banca tende a fundir. A primeira é **inclusão no modelo**: as treze linhas com “Sim” em “No modelo?” entram simultaneamente no Logit, porque esse é o conjunto a priori do Cleveland de 14 atributos e porque o contraste bruto versus ajustado exige que as variáveis “fracas” no final também tenham sido controladas. A segunda é **ênfase na narrativa**: apenas cinco recebem parágrafos longos no Capítulo 4, para atender ao pedido de analisar com critério um núcleo interpretativo sem fingir que as outras não existem.

Não se reduz o Logit às cinco porque idade, `oldpeak` e `chol` só mostram o apagamento condicional se estiverem no modelo; porque o conjunto de 13 não foi escolhido depois de ver os p-valores; e porque o EPV próximo de 10,5 não autoriza, por si, seleção dirigida pelo resultado. `exang` e `trestbps` são significativas no ajuste e **não foram excluídas**; apenas não repetem a mesma extensão de parágrafo, pois a narrativa privilegiou `ca` (magnitude), `sex` (hipótese), `cp` (codificação), `thal` (exame) e `thalach` (anti-correlação).

## 3.6 Análise descritiva e bivariada

A etapa descritiva responde ao objetivo específico (a): quem é a amostra depois do `dropna`. Reportam-se N, prevalência do desfecho, médias e desvios-padrão das contínuas e distribuições das categóricas. Sem essa fotografia, os p-valores posteriores não têm denominador clínico.

A etapa bivariada responde ao objetivo (b) e alimenta o contraste do Capítulo 4. Spearman foi calculado entre `target` e `age`, `trestbps`, `chol`, `thalach`, `oldpeak` e `ca` — contínuas e a contagem ordinal de vasos. Qui-quadrado de Pearson foi aplicado a `sex`, `cp`, `fbs`, `restecg`, `exang`, `slope` e `thal`. O OR bruto de sexo usou a tabela 2×2 na ordem masculino/feminino × doente/não doente, como exemplo de magnitude sem ajuste, a ser confrontado com o coeficiente de `sex` no Logit.

O nível descritivo de significância na apresentação é α = 0,05. Não se aplicou correção formal para multiplicidade na bivariada, porque essa etapa é exploratória em relação ao modelo ajustado, que é o teste das hipóteses da seção 1.3. Essa escolha deve ser dita à banca: a bivariada descreve; o Logit decide a H0 global.

## 3.7 Modelo logístico e hipóteses

O modelo estimado é a regressão logística binária, com intercepto e as 13 preditoras em escala numérica, alinhado ao objetivo (c) e às hipóteses da seção 1.3. A função de ligação é o logito; a estimação, por máxima verossimilhança. Reportam-se convergência, log-verossimilhança, teste de razão de verossimilhança contra o modelo nulo (somente intercepto), pseudo-R² de McFadden e testes de Wald por coeficiente, com intervalos de confiança de 95%.

A H0 global afirma que todos os coeficientes das preditoras são nulos após o ajuste. A H1 afirma que pelo menos um não o é. A hipótese específica recai sobre `sex`. Não se pré-especificou uma bateria de treze testes confirmatórios; os p-valores individuais são descritivos do ajuste, e a ênfase nas cinco variáveis da Tabela 1 é interpretativa.

## 3.8 Avaliação do modelo (ROC/AUC e Brier)

Esta seção operacionaliza o objetivo (d). Depois do ajuste, cada observação recebe uma probabilidade predita π̂ᵢ. Variando o limiar sobre π̂, constrói-se a curva ROC e calcula-se a AUC, medida de discriminação (HANLEY; MCNEIL, 1982). O Brier do modelo é a média de (π̂ᵢ − yᵢ)². O Brier nulo usa π̂ᵢ = ȳ (prevalência amostral) para todo i, de modo que o ganho seja relativo a “prever sempre a prevalência”, e não um número isolado (BRIER, 1950; STEYERBERG, 2019).

A curva ROC figura no Apêndice B. Ambos os índices são **in-sample**: calculados na mesma amostra do ajuste. Essa decisão é explícita e limita a generalização; não é um detalhe a esconder no rodapé. Validação cruzada permanece como trabalho futuro, sem alteração do modelo de 13 preditoras.

## 3.9 Aspectos éticos (dados secundários anonimizados)

O repositório UCI disponibiliza o conjunto sem identificadores nominais; nomes e números de segurança social foram removidos na origem (JÁNOSI et al., 1989). Não se aplica coleta em seres humanos pelo autor, nem termo de consentimento individual neste mestrado, porque não há intervenção nem acesso a prontuário.

O uso declarado é de pesquisa metodológica e ensino de modelagem. O modelo **não** se destina a decidir cateterismo, prescrição ou triagem em serviço de saúde brasileiro. Essa fronteira ética é também uma fronteira científica: dados históricos de um único centro norte-americano não autorizam protocolo assistencial.

## 3.10 Limitações metodológicas previstas

As limitações abaixo foram antecipadas **antes** da leitura dos resultados, para que o Capítulo 4 não as invente à medida que os p-valores aparecem.

A amostra é histórica e não brasileira; prevalências e coeficientes não se transportam ao SUS. A análise é de casos completos: registros com falha em `ca`, `thal` ou `slope` saem, o que pode viesar se o missing não for aleatório. O EPV situa-se próximo do limiar clássico de dez eventos por variável (PEDUZZI et al., 1996). Códigos ordinais entram como numéricos. AUC e Brier são in-sample. O pipeline atual não calcula VIF nem validação cruzada — diagnósticos úteis à defesa, que não trocam o modelo principal. Não há pretensão causal: o Logit estima associações condicionais à especificação.

Essas restrições não anulam o protocolo; delimitam o que a Conclusão pode afirmar.

---

# 4 RESULTADOS E DISCUSSÃO

Este capítulo cumpre o encargo de “vender o peixe”: diz o que foi executado (4.1), o que se esperava encontrar à luz das hipóteses (4.2) e, em seguida, o que os dados mostraram — amostra (4.3), bivariada (4.4), Logit e contraste bruto versus ajustado (4.5), as cinco variáveis de ênfase (4.6), ROC e Brier (4.7) e a leitura clínica cautelosa da codificação UCI (4.8). Os números completos estão no Apêndice A; o texto abaixo interpreta, não substitui as tabelas.

## 4.1 O que foi feito e como foi feito (protocolo executado)

Esta seção não discute p-valores; documenta a execução. Foi corrido, de ponta a ponta, o protocolo do Capítulo 3, sem atalhos de seleção de variáveis e sem inclusão de métodos recusados na seção 3.4.

Utilizou-se o export do repositório UCI, reteve-se o subconjunto Cleveland, recodificou-se para os códigos da documentação, dicotomizou-se `num` em `target` e excluiu-se missing em `ca`, `thal` e `slope`. Sobre N = 297, calculou-se a descritiva, Spearman, qui-quadrado, OR bruto de sexo, logística com 13 preditoras e intercepto, AUC, Brier do modelo e Brier nulo, e gravou-se a curva ROC. O software foi Python, com `pandas`, `scipy`, `statsmodels` e `scikit-learn`. Não se aplicou DFA, DCCA, Cox, stepwise nem classificadores de ML. Não se reduziu o Logit a cinco variáveis.

O que segue, portanto, é o produto desse protocolo — não de uma especificação escolhida depois de olhar o resultado.

## 4.2 O que se esperava encontrar

Antes de abrir as tabelas, convém fixar o que as hipóteses e a fundamentação antecipavam. Sem isso, qualquer coeficiente “significativo” parece sucesso e qualquer coeficiente nulo parece fracasso.

Esperava-se, em primeiro lugar, **rejeitar a H0 global**: o conjunto clássico de atributos Cleveland não deveria ser ruído puro após o ajuste (DETRANO et al., 1989; AMZAD HOSSEN et al., 2021). Esperava-se, em segundo lugar, que **nem toda associação bruta sobrevivesse** ao Logit — em particular idade e marcadores de esforço correlacionados entre si. Esperava-se que o sexo masculino mantivesse associação positiva (hipótese específica) e que `thalach` pudesse exibir sinal negativo (maior frequência máxima, menor odds de doença). Esperava-se AUC claramente acima de 0,5 e Brier do modelo inferior ao nulo, com a ressalva de otimismo in-sample já anunciada na seção 3.8.

Encontrar exatamente esse padrão — H0 rejeitada, parte da bivariada apagada, `sex` e `thalach` com os sinais previstos — é o critério de êxito do desenho, não uma AUC isolada de 0,925.

## 4.3 Caracterização da amostra

A caracterização corresponde ao objetivo específico (a) e serve de denominador para tudo o que vem depois. Sem N, prevalência e perfil demográfico, Spearman e OR não têm contexto.

A amostra analítica tem **297** pacientes. Sem doença (`target = 0`): **160** (53,9%). Com doença (`target = 1`): **137** (46,1%). A prevalência 0,461 alimenta o Brier nulo da seção 4.7.

A idade média foi 54,54 anos (DP 9,05; mínimo 29; máximo 77). A pressão de repouso média foi 131,69 mmHg (DP 17,76); o colesterol médio, 247,35 mg/dL (DP 52,00); `oldpeak` médio 1,06 (DP 1,17); `ca` médio 0,68 (DP 0,94). Aproximadamente 67,7% da amostra é do sexo masculino (`sex` médio 0,68). A frequência máxima média é compatível com teste ergométrico em população de meia-idade. Detalhes figuram no Apêndice A.

O perfil é o esperado para o Cleveland clássico: maioria masculina, idade média na quinta década, desfecho quase equilibrado. Não se infere prevalência brasileira a partir desses percentuais. O equilíbrio aproximado do desfecho, contudo, é favorável à logística e ao Brier: não se está diante de um evento raríssimo na amostra.

## 4.4 Associações bivariadas

A bivariada cumpre o objetivo (b) e cria o painel bruto que o Logit vai, em seguida, confirmar ou desfazer. Spearman informa sinal e força monotônica; o qui-quadrado informa dependência em tabelas, sem direção; o OR de sexo informa magnitude em escala de chances, ainda sem covariáveis.

**Spearman.** Todas as seis comparações contínuas/`ca` versus `target` foram significativas a 5%:

- `ca`: ρ = 0,492 (p < 0,001) — associação positiva mais forte;
- `oldpeak`: ρ = 0,411 (p < 0,001);
- `age`: ρ = 0,240 (p = 0,00003);
- `trestbps`: ρ = 0,132 (p = 0,023);
- `chol`: ρ = 0,116 (p = 0,046) — limítrofe;
- `thalach`: ρ = **−0,429** (p < 0,001) — **anti-correlação**.

O sinal de `thalach` confirma que o protocolo não caça apenas correlações positivas: maior frequência máxima no esforço associa-se a menor presença de doença na bivariada, coerente com melhor capacidade funcional.

**Qui-quadrado.** Houve associação com `sex` (χ² = 21,85; p = 2,95 × 10⁻⁶), `cp` (χ² = 77,28; p = 1,18 × 10⁻¹⁶), `restecg` (χ² = 9,58; p = 0,008), `exang` (χ² = 50,94; p = 9,51 × 10⁻¹³), `slope` (χ² = 43,47; p = 3,63 × 10⁻¹⁰) e `thal` (χ² = 82,46; p = 1,24 × 10⁻¹⁸). **`fbs` não se associou** (χ² ≈ 0; p = 1,0). Esse nulo bivariado deve ser lembrado quando o Logit devolver p = 0,066 para `fbs`: não se inventa uma história clínica forte para glicemia de jejum neste recorte.

**OR bruto de sexo.** OR ≈ **3,57** (homens versus mulheres, sem ajuste). Homens concentram maior *odds* bruta de doença na tabela 2×2. A seção 4.5 verifica se isso sobrevive ao controle pelas demais preditoras — que é exatamente a hipótese específica.

## 4.5 Modelo ajustado e contraste bruto versus independente

Esta seção é o núcleo inferencial: testa a H0 global, descreve quais coeficientes sobrevivem e confronta esse quadro com a bivariada da seção 4.4. O “peixe” a vender não é a lista de p-valores, e sim o **apagamento seletivo** de associações brutas.

O Logit convergiu (7 iterações). Log-verossimilhança = −102,34; modelo nulo ℓ = −204,97; **pseudo-R² de McFadden = 0,501**; teste LR: **p = 1,14 × 10⁻³⁶**. Rejeita-se a H0 global com folga. A hipótese alternativa de que pelo menos uma preditora se associa independentemente é sustentada pelos dados desta amostra.

Coeficientes de Wald (sinal, p-valor):

- significativos a 5%: `sex` (+1,31; p = 0,007), `cp` (+0,58; p = 0,003), `trestbps` (+0,024; p = 0,025), `thalach` (−0,021; p = 0,043), `exang` (+0,93; p = 0,025), `ca` (+1,27; p < 0,001), `thal` (+0,34; p = 0,001);
- limítrofe: `fbs` (−1,02; p = 0,066);
- não significativos: `age` (−0,014; p = 0,555), `chol` (+0,005; p = 0,186), `restecg` (+0,25; p = 0,185), `oldpeak` (+0,25; p = 0,243), `slope` (+0,57; p = 0,116).

O **contraste bruto versus ajustado** é o resultado a vender. Idade, `oldpeak` e colesterol associam-se na bivariada e **não** se sustentam no Logit. `restecg` e `slope` igualmente perdem o protagonismo. `sex` e `ca` permanecem. `thalach` mantém o sinal negativo. Isso é exatamente o padrão esperado na seção 4.2: confundimento e sobreposição de informação de esforço (`oldpeak`, `slope`, `thalach`, `exang`), não a tese de que “idade não importa na clínica”. Na clínica, idade importa; **neste modelo condicional a exames que já carregam gravidade**, o coeficiente de idade se aproxima de zero.

O OR bruto de sexo (~3,57) e o coeficiente ajustado positivo (p = 0,007) caminham na mesma direção: a hipótese específica não é rejeitada. O valor pontual do OR ajustado, exp(1,312) ≈ 3,71, é da mesma ordem do bruto; o intervalo de confiança do coeficiente (0,355 a 2,269 na escala do logito) exclui o zero. A dissertação não afirma que o OR ajustado “é 3,71 na população mundial”; afirma que, **neste ajuste, nesta amostra**, o sexo masculino permanece associado a maior odds.

## 4.6 Ênfase interpretativa nas cinco variáveis destacadas

A Tabela 1 reservou cinco preditoras para desenvolvimento mais longo. O que segue não as promove a “único modelo verdadeiro”; apenas organiza a discussão na ordem de critério: magnitude (`ca`), hipótese (`sex`), codificação (`cp`), exame (`thal`) e sinal negativo (`thalach`).

**`ca`.** É a associação ajustada mais nítida. Cada vaso adicional corado eleva o logito em cerca de 1,27. Spearman já apontava ρ = 0,49. A proximidade conceitual com o desfecho angiográfico recomenda humildade: parte da “previsão” é quase tautológica. Ainda assim, no protocolo de 14 atributos, omitir `ca` seria omitir o preditor dominante e distorcer os demais coeficientes.

**`sex`.** Homens têm maior odds bruta e ajustada. A hipótese específica encontra apoio. O mecanismo (exposição, biologia, viés de referência ao cateterismo na década original) **não** é identificável aqui.

**`cp`.** Coeficiente positivo: códigos UCI mais altos associam-se a maior odds. O ponto crítico para a banca é o código **4 = assintomático**. No Cleveland, a categoria assintomática concentra risco angiográfico, o oposto da intuição “quem não tem dor está melhor”. Interpretar `cp` como escala de gravidade da dor é erro. Interpretar como códigos nominais ordenados pela documentação UCI é o que o modelo faz.

**`thal`.** Códigos 3/6/7 tratados linearmente: o coeficiente positivo indica tendência de maior odds ao caminhar rumo ao defeito reversível. A interpolação entre 3 e 6 não é anatomicamente “duas vezes 3”. A significância (p = 0,001) justifica a ênfase; a escala justifica a limitação.

**`thalach`.** Anti-correlação na bivariada e β negativo no Logit (p = 0,043). Maior frequência máxima atingida associa-se a menor odds de doença, condicional às demais. É o exemplo de que o trabalho olha o sinal, não só o “fator de risco positivo”.

`exang` e `trestbps` também são significativos e **não foram retirados**. Apenas não repetem o mesmo desenvolvimento de parágrafo, para cumprir o pedido de ênfase em cinco sem fingir que as outras não existem.

## 4.7 Desempenho (ROC e Brier) e leitura cautelosa (in-sample)

Coeficientes significativos não garantem, por si, que as probabilidades separem bem os grupos ou se aproximem do desfecho. Por isso o protocolo inclui ROC/AUC e Brier, como previsto no objetivo (d) e na seção 3.8.

A AUC in-sample foi **0,925**. A curva (Apêndice B) afasta-se da diagonal. Em linguagem de Hanley e McNeil (1982), o modelo ordena bem casos e não casos **na amostra em que foi treinado**.

O Brier do Logit foi **0,107**; o Brier nulo (prevalência 0,461) foi **0,249**. Há redução substancial do erro quadrático frente a prever sempre 46,1%. Isso responde à pergunta do orientador: o Brier cabe, é interpretável e não compete com a ROC — mede outra coisa (BRIER, 1950; STEYERBERG, 2019; HOESSLY, 2025).

A leitura honesta: 0,925 **não** é uma AUC de validação externa nem de validação cruzada. Métricas in-sample tendem a ser otimistas (STEYERBERG, 2019). A dissertação não esconde esse ponto; ele é parte do resultado. Trabalho futuro imediato, sem trocar o modelo de 13 preditoras, é reportar AUC e Brier em validação cruzada.

## 4.8 Discussão à luz da literatura e da lógica clínica da codificação UCI

Fechados os números, resta situá-los: o que é coerente com a literatura do Cleveland, o que depende da codificação UCI e o que este mestrado **não** pode afirmar.

Os achados alinham-se à literatura que usa o Cleveland como banco de classificação e encontra poder discriminativo elevado para a logística (AMZAD HOSSEN et al., 2021), mas deslocam o centro do argumento: o valor está no **apagamento seletivo** de associações brutas e na persistência de `sex`, `ca`, `cp`, `thal` e `thalach`.

Clinicamente, vasos corados, sexo masculino, padrão de dor na codificação UCI, cintilografia e baixa frequência máxima são coerentes com o conhecimento coronariano clássico (DETRANO et al., 1989) — **desde que** `cp = 4` não seja lido como proteção. Estatisticamente, o EPV ~10,5 e o complete-case aconselham não superinterpretar coeficientes limítrofes (`fbs`).

Não se extrapola para o Brasil, para a década de 2020, nem para decisão de cateterismo. O estudo vende um protocolo e um contraste, não um escore assistencial. Essa contenção é o que torna o Capítulo 4 defensável.

---

# 5 CONCLUSÃO

Este capítulo não apresenta tabelas novas. Retoma o Resumo em texto contínuo: o que foi feito, como, se o que se esperava ocorreu, se a metodologia foi a indicada, e o que permanece aberto.

Identificaram-se associações entre variáveis clínicas e de exame e a presença de doença cardíaca no subconjunto Cleveland do repositório UCI, contrastando análise bivariada e regressão logística binária. Avaliou-se o modelo pela curva ROC (AUC) e pelo Brier score, este último comparado ao modelo nulo de prevalência constante. A amostra analítica teve 297 pacientes (160 sem doença angiográfica significativa; 137 com doença). Cinco preditoras foram privilegiadas na interpretação (`ca`, `sex`, `cp`, `thal` e `thalach`), **sem** exclusão das outras oito do ajuste. Esse é o objeto cumprido, nos termos do objetivo geral da seção 1.2.

O caminho foi o da seção 3.4. Dados secundários públicos foram recodificados para os códigos numéricos UCI. Spearman descreveu associações monotônicas, inclusive negativas. Qui-quadrado testou as categóricas. Um OR bruto exemplificou o efeito de sexo sem covariáveis. O modelo logístico com 13 preditoras e intercepto produziu efeitos ajustados e o teste de razão de verossimilhança da H0 global. AUC e Brier (modelo e nulo) resumiram discriminação e erro quadrático na amostra do ajuste. DFA, DCCA, Cox, Pearson como método principal, mínimos quadrados ordinários, *stepwise* e aprendizado de máquina não foram aplicados, pelos critérios já expostos: desfecho binário, corte transversal e pergunta de associação — não de série temporal, nem de ranking de acurácia.

No recorte declarado na seção 4.2, os resultados esperados ocorreram. A H0 global foi rejeitada (p = 1,14 × 10⁻³⁶; pseudo-R² = 0,50). A hipótese específica de `sex` não foi rejeitada (p = 0,007; OR bruto ≈ 3,57 na mesma direção). Parte das associações brutas **não** se sustentou (`age`, `oldpeak`, `chol`, entre outras), o que era esperado como manifestação de confundimento e de sobreposição entre marcadores de esforço. `thalach` apresentou anti-correlação e coeficiente negativo no modelo ajustado. A AUC (0,925) e a queda do Brier (0,107 versus 0,249) ocorreram, com a limitação in-sample já prevista. `fbs` permaneceu sem associação bivariada e apenas limítrofe na logística, o que impede uma narrativa forçada. Encontrou-se, portanto, o padrão anunciado — rejeição da H0, contraste bruto versus ajustado, sinal de `thalach` — e não um achado extra incompatível com o desenho.

Para um desfecho binário, pergunta de associação bruta versus independente e dados transversais, a logística foi a ferramenta indicada (HOSMER; LEMESHOW; STURDIVANT, 2013; SCHOBER; VETTER, 2021). Spearman e qui-quadrado são os pares bivariados adequados aos tipos de variável. ROC e Brier são complementares e pertinentes; o Brier cabe e não concorre com a AUC. DFA e DCCA não seriam mais indicados: serviriam a séries, que este banco não é. Aprendizado de máquina não seria mais indicado como núcleo, porque deslocaria o objeto de OR ajustado para acurácia. Reduzir o modelo a cinco preditoras também não seria mais indicado: destruiria o contraste que a dissertação se propôs a mostrar. “Mais indicada” não significa sem limitações; significa adequação ao desenho, ao desfecho e à pergunta, com exclusões justificadas na seção 3.4.

As limitações antecipadas na seção 3.10 confirmam-se após os resultados. Os dados são históricos e não brasileiros. A análise é de casos completos. O EPV está no limiar clássico. Códigos ordinais foram tratados como numéricos. AUC e Brier são in-sample. Não se calculou VIF nem validação cruzada. Não há identificação causal. Os trabalhos futuros, sem abandonar o modelo de 13 preditoras, são validação cruzada de AUC e Brier, cálculo de VIF, revisão Scopus institucional 2021–2026, análise de sensibilidade com variáveis dummy para `cp` e `thal` em apêndice e, apenas se o orientador o solicitar, comparação preditiva com um único algoritmo de aprendizado de máquina, claramente separada do núcleo associativo.

A pergunta aberta na Introdução foi respondida no recorte possível: a metodologia foi a adequada a esse recorte, e o que não se pode afirmar ficou explícito.

---

# REFERÊNCIAS

As referências seguem o sistema autor-data, em ordem alfabética, conforme a ABNT. Incluem fundamentos clássicos (Spearman, Brier, logística, Cleveland/UCI) e itens de 2021–2025 para a revisão recente. Entradas cuja paginação ou volume não foram conferidos no PDF oficial da base institucional estão marcadas com `[VERIFICAR NO SCOPUS]`. A lista abaixo é a citada no corpo; a exportação completa do Scopus da biblioteca deve substituir ou complementar estes itens na versão final.

AMZAD HOSSEN, M. D. *et al.* Supervised machine learning-based cardiovascular disease analysis and prediction. **Mathematical Problems in Engineering**, v. 2021, artigo 1792201, 2021. DOI: https://doi.org/10.1155/2021/1792201.

BRIER, G. W. Verification of forecasts expressed in terms of probability. **Monthly Weather Review**, v. 78, n. 1, p. 1-3, 1950.

DETRANO, R. *et al.* International application of a new probability algorithm for the diagnosis of coronary artery disease. **The American Journal of Cardiology**, v. 64, n. 5, p. 304-310, 1989. DOI: https://doi.org/10.1016/0002-9149(89)90524-9.

HANLEY, J. A.; MCNEIL, B. J. The meaning and use of the area under a receiver operating characteristic (ROC) curve. **Radiology**, v. 143, n. 1, p. 29-36, 1982.

HOESSLY, L. On misconceptions about the Brier score in binary prediction models. **Global Epidemiology**, artigo 100242, 2025. DOI: https://doi.org/10.1016/j.gloepi.2025.100242. `[VERIFICAR NO SCOPUS volume e páginas]`

HOSMER, D. W.; LEMESHOW, S.; STURDIVANT, R. X. **Applied logistic regression**. 3. ed. Hoboken: Wiley, 2013.

JÁNOSI, A.; STEINBRUNN, W.; PFISTERER, M.; DETRANO, R. **Heart Disease**. Irvine: UCI Machine Learning Repository, 1989. DOI: https://doi.org/10.24432/C52P4X.

ORGANIZAÇÃO MUNDIAL DA SAÚDE. **Cardiovascular diseases (CVDs)**. Genebra: WHO, 2021. Disponível em: https://www.who.int/news-room/fact-sheets/detail/cardiovascular-diseases-(cvds). Acesso em: 16 ago. 2026. `[VERIFICAR NO SCOPUS / data da ficha atualizada]`

PEDUZZI, P.; CONCATO, J.; KEMPER, E.; HOLFORD, T. R.; FEINSTEIN, A. R. A simulation study of the number of events per variable in logistic regression analysis. **Journal of Clinical Epidemiology**, v. 49, n. 12, p. 1373-1379, 1996.

PENG, C. K.; BULDYREV, S. V.; HAVLIN, S.; SIMONS, M.; STANLEY, H. E.; GOLDBERGER, A. L. Mosaic organization of DNA nucleotides. **Physical Review E**, v. 49, n. 2, p. 1685-1689, 1994.

PENG, C. Y. J.; LEE, K. L.; INGERSOLL, G. M. An introduction to logistic regression analysis and reporting. **The Journal of Educational Research**, v. 96, n. 1, p. 3-14, 2002.

PODOBNIK, B.; STANLEY, H. E. Detrended cross-correlation analysis: a new method for analyzing two nonstationary time series. **Physical Review Letters**, v. 100, n. 8, 084102, 2008.

SCHOBER, P.; VETTER, T. R. Logistic regression in medical research. **Anesthesia & Analgesia**, v. 132, n. 2, p. 365-366, 2021. DOI: https://doi.org/10.1213/ANE.0000000000005247.

SPEARMAN, C. The proof and measurement of association between two things. **The American Journal of Psychology**, v. 15, n. 1, p. 72-101, 1904.

STEYERBERG, E. W. **Clinical prediction models**: a practical approach to development, validation, and updating. 2. ed. Cham: Springer, 2019.

VANDERWEELE, T. J. Principles of confounder selection. **European Journal of Epidemiology**, v. 34, n. 3, p. 211-219, 2019.

ZEBENDE, G. F. DCCA cross-correlation coefficient: quantifying level of cross-correlation. **Physica A: Statistical Mechanics and its Applications**, v. 390, n. 4, p. 614-618, 2011.

---

# APÊNDICE A — Tabelas numéricas geradas pelo código

Este apêndice reúne as saídas numéricas da análise sobre o subconjunto Cleveland, após exclusão de valores em falta em `ca`, `thal` e `slope`. O corpo dos capítulos interpreta esses números; aqui eles aparecem em formato de tabela. A seção A.1 descreve o desfecho; a A.2, as médias; a A.3, Spearman; a A.4, o qui-quadrado; a A.5, o OR bruto de sexo; a A.6, o Logit; a A.7, AUC e Brier. Scripts e tabelas de replicação estão no repositório do autor.

**A.1 Amostra e desfecho**

A Tabela A.1 fixa o denominador da dissertação: 297 observações e desfecho quase equilibrado, com prevalência 0,4613 usada no Brier nulo.

| Item | Valor |
| --- | --- |
| N | 297 |
| target = 0 | 160 (53,9%) |
| target = 1 | 137 (46,1%) |
| Prevalência | 0,4613 |

**A.2 Descritiva (média e DP)**

A Tabela A.2 resume as contínuas e a proporção de homens. Idade média na quinta década e maioria masculina são o perfil clássico do Cleveland, não uma amostra brasileira.

| Variável | Média | DP |
| --- | --- | --- |
| age | 54,54 | 9,05 |
| trestbps | 131,69 | 17,76 |
| chol | 247,35 | 52,00 |
| oldpeak | 1,06 | 1,17 |
| ca | 0,68 | 0,94 |
| sex (proporção masculina) | 0,68 | 0,47 |

**A.3 Spearman versus target**

A Tabela A.3 documenta sinal e força brutos. Destacam-se `ca` (ρ = 0,492) e a anti-correlação de `thalach` (ρ = −0,429). Colesterol é limítrofe (p = 0,046).

| Variável | ρ | p |
| --- | --- | --- |
| age | 0,240 | 0,00003 |
| trestbps | 0,132 | 0,02317 |
| chol | 0,116 | 0,04643 |
| thalach | −0,429 | < 0,001 |
| oldpeak | 0,411 | < 0,001 |
| ca | 0,492 | < 0,001 |

**A.4 Qui-quadrado versus target**

A Tabela A.4 mostra dependência nas categóricas, com exceção de `fbs` (p = 1). O teste não informa direção; esta vem do Logit ou dos percentuais.

| Variável | χ² | p |
| --- | --- | --- |
| sex | 21,852 | 2,95 × 10⁻⁶ |
| cp | 77,276 | 1,18 × 10⁻¹⁶ |
| fbs | 0,000 | 1,000 |
| restecg | 9,576 | 0,00833 |
| exang | 50,943 | 9,51 × 10⁻¹³ |
| slope | 43,473 | 3,63 × 10⁻¹⁰ |
| thal | 82,460 | 1,24 × 10⁻¹⁸ |

**A.5 OR bruto sexo × target**

O odds ratio bruto (masculino versus feminino) é aproximadamente **3,574**. Esse número não está ajustado; o coeficiente de `sex` no Logit (Tabela A.6) é o análogo condicional.

**A.6 Logística (coeficientes; extraído do `summary`)**

A Tabela A.6 reproduz o ajuste principal. O intercepto é negativo e significativo. Rejeita-se a H0 global (LLR p = 1,136 × 10⁻³⁶; pseudo-R² = 0,5007). OR ajustados na escala exp(β) obtêm-se exponenciando os coeficientes e os limites do intervalo de confiança.

| Variável | Coef. | EP | z | p | IC95% coef. |
| --- | --- | --- | --- | --- | --- |
| const | −7,372 | 2,879 | −2,56 | 0,010 | −13,016 ; −1,728 |
| age | −0,014 | 0,024 | −0,59 | 0,555 | −0,061 ; 0,033 |
| sex | 1,312 | 0,488 | 2,69 | 0,007 | 0,355 ; 2,269 |
| cp | 0,576 | 0,191 | 3,01 | 0,003 | 0,201 ; 0,951 |
| trestbps | 0,024 | 0,011 | 2,24 | 0,025 | 0,003 ; 0,045 |
| chol | 0,005 | 0,004 | 1,32 | 0,186 | −0,002 ; 0,012 |
| fbs | −1,022 | 0,555 | −1,84 | 0,066 | −2,110 ; 0,067 |
| restecg | 0,245 | 0,185 | 1,33 | 0,185 | −0,117 ; 0,608 |
| thalach | −0,021 | 0,010 | −2,02 | 0,043 | −0,041 ; −0,001 |
| exang | 0,926 | 0,413 | 2,24 | 0,025 | 0,116 ; 1,736 |
| oldpeak | 0,247 | 0,212 | 1,17 | 0,243 | −0,168 ; 0,663 |
| slope | 0,570 | 0,363 | 1,57 | 0,116 | −0,142 ; 1,282 |
| ca | 1,268 | 0,265 | 4,78 | < 0,001 | 0,748 ; 1,788 |
| thal | 0,344 | 0,100 | 3,43 | 0,001 | 0,147 ; 0,541 |

Pseudo-R² (McFadden) = 0,5007. LLR p = 1,136 × 10⁻³⁶.

**A.7 Desempenho in-sample**

A Tabela A.7 resume discriminação e erro quadrático na amostra do ajuste. A AUC 0,925 e o Brier 0,107 (versus 0,2485 no nulo) devem ser lidos com a ressalva de otimismo in-sample, já discutida na seção 4.7.

| Métrica | Valor |
| --- | --- |
| AUC | 0,9246 |
| Brier (modelo) | 0,1069 |
| Brier (nulo, prevalência 0,4613) | 0,2485 |

OR ajustados e IC95% na escala exp(β) obtêm-se exponenciando os coeficientes e os limites do intervalo de confiança reportados na Tabela A.6.

---

# APÊNDICE B — Figura da curva ROC

Este apêndice contém a única figura prevista no sumário. A curva ROC traduz, graficamente, a AUC reportada na seção 4.7 e na Tabela A.7. Não substitui o Brier: mostra ordenação, não o erro quadrático das probabilidades.

**Figura 1 — Curva ROC do modelo logístico binário (amostra completa, in-sample).**

Inserir no Word a figura da curva ROC produzida na análise. Eixo X: taxa de falsos positivos. Eixo Y: taxa de verdadeiros positivos. A linha tracejada é a referência de um classificador aleatório (AUC = 0,5). A AUC observada é aproximadamente 0,925.

Legenda para o Word: “Curva ROC do modelo com 13 preditoras e intercepto, estimada na mesma amostra do ajuste (N = 297). A discriminação in-sample tende a ser otimista para generalização.”

Após inserir a figura, conferir se a numeração (Figura 1) coincide com a lista de ilustrações dos pré-textuais.
