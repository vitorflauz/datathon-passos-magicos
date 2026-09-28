# Datathon Fase 5: Passos Mágicos

Trabalho do Datathon da Fase 5 da pós em Data Analytics da FIAP POSTECH. Analisamos os indicadores do PEDE de 2022 a 2024 da Associação Passos Mágicos e construímos um modelo que aponta, com um ano de antecedência, os alunos com risco de entrar em defasagem. O modelo está disponível num app em Streamlit.

A apresentação está em [entrega/apresentacao_passos_magicos.pdf](entrega/apresentacao_passos_magicos.pdf).

## Principais resultados

A proporção de alunos na fase esperada para a idade subiu de 30% em 2022 para 49% em 2024. Entre os alunos presentes nos três anos, foi de 34% para 63%.

Por outro lado, 30% dos alunos repetem a fase a cada ano, e isso acontece mais com quem está em fase (43%) do que com quem já está atrasado (23%).

O modelo prevê quem vai entrar em defasagem ou aprofundá-la no ano seguinte. No ano de teste (2023 para 2024), identificou 74% desses alunos sinalizando 23% da base, com AUC de 0,89 (IC 95% de 0,86 a 0,93). Testamos sete algoritmos: Random Forest, Extra Trees e Gradient Boosting empataram no topo e ficaram acima da Regressão Logística (AUC 0,81 no teste). O modelo acerta mais na ALFA (92% dos casos) do que nas fases 3 a 5 (40%).

## Pastas

```
app/          app Streamlit (app.py)
dados/        base original do PEDE; dados/tratados/ tem a base limpa (pede_long.csv)
figuras/      gráficos salvos pelos notebooks
modelos/      modelo treinado (modelo_risco.joblib) e métricas (modelo_info.json)
notebooks/    01 limpeza, 02 análise exploratória, 03 modelo preditivo
src/          features.py, usado pelo notebook 03 e pelo app
```

O notebook 02 responde às perguntas 1 a 8, 10 e 11 do desafio, e o 03 responde à pergunta 9.

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/app.py
```

No Mac ou Linux, ative o ambiente com `source .venv/bin/activate`.

Os notebooks devem ser executados na ordem 01, 02 e 03. O 01 gera `dados/tratados/pede_long.csv` e o 03 gera `modelos/modelo_risco.joblib`. Os dois arquivos já estão no repositório, então o app funciona sem rodar os notebooks.

## Decisões de modelagem

O alvo é a defasagem (fase − fase ideal) piorar de um ano para o seguinte com o aluno terminando atrasado. Os indicadores do ano *t* preveem o que acontece em *t+1*. IAN, INDE e Pedra ficaram fora das variáveis porque são recodificações da defasagem ou combinações fixas dos indicadores, e usá-los seria vazamento.

A validação é temporal: treino com os pares 2022-2023 e teste com 2023-2024. O Random Forest com classes balanceadas foi escolhido entre sete algoritmos pela validação cruzada no treino, e o limiar também foi definido no treino, para recall de 75%.

A probabilidade do modelo ordena bem os alunos, mas superestima o risco abaixo de 0,6 por causa do balanceamento de classes. Por isso, no app, ela é usada para priorizar a lista.

## Deploy

O app roda no Streamlit Community Cloud com `app/app.py` como arquivo principal e Python 3.12. O `scikit-learn` está fixado em 1.8.0 no `requirements.txt` porque o modelo salvo precisa ser carregado com a mesma versão em que foi treinado.
