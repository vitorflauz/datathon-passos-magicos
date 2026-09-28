# Roteiro do vídeo (até 5 minutos)

São cerca de 610 palavras, perto de 5 minutos em ritmo normal, contando as trocas de slide e a demonstração do app. O vídeo vai do slide 1 ao 16; o apêndice (slides 17 a 22) fica para consulta.

**[0:00 a 0:15] Slide 1 · Capa**

A Passos Mágicos atende crianças e jovens de baixa renda em Embu-Guaçu e acompanha cada aluno pelo PEDE. Analisamos três anos de dados para responder às onze perguntas do desafio.

**[0:15 a 0:40] Slide 2 · Resumo executivo**

Começamos pela recomendação. O programa reduz a defasagem, mas três em cada dez alunos repetem a fase por ano, e isso acontece mais com quem está em dia. Propomos usar um modelo que antecipa esses alunos no início do ano e ajustar a medição. A decisão que pedimos é adotar a lista de 2025 como ranking de acompanhamento.

**[0:40 a 1:05] Slide 3 · Fase e defasagem**

Antes dos resultados, alguns conceitos. Os alunos são organizados em fases, da ALFA, que é a alfabetização, até a fase 7, o 3º ano do ensino médio. Cada idade tem uma fase ideal, e a defasagem é a fase atual menos a ideal: um aluno de 12 anos na fase 2 tem defasagem −1. Quando o aluno repete a fase, a idade avança e ele fica mais atrasado.

**[1:05 a 1:15] Slide 4 · Indicadores**

O PEDE avalia cada aluno em sete indicadores, de zero a dez. O INDE é a nota global, e a pedra é a faixa dessa nota.

**[1:15 a 1:35] Slide 5 · O que funciona**

A proporção de alunos em fase subiu de 30% para 49%. Entre os 441 alunos presentes nos três anos, foi de 34% para 63%, então a melhora não vem da troca de turma. Os alunos chegam atrasados, e o programa reduz esse atraso.

**[1:35 a 1:55] Slide 6 · Retenção**

A retenção se concentra na ALFA e na fase 5. E 43% dos alunos em fase repetem a fase, contra 23% dos já atrasados. Ou seja, a defasagem costuma começar em alunos que hoje parecem estar bem.

**[1:55 a 2:15] Slide 7 · Sinais antecedentes**

Alguns sinais aparecem um ano antes. Entre os alunos com o indicador psicossocial mais baixo, 33% perdem engajamento no ano seguinte, quase três vezes o observado no terceiro grupo.

**[2:15 a 2:30] Slide 8 · Desempenho acadêmico**

O desempenho acadêmico está estagnado, com queda em Português em 2024, e é mais baixo entre o 5º e o 9º ano. É o indicador que mais pesa nas diferenças de INDE.

**[2:30 a 2:50] Slide 9 · Medição**

A autoavaliação não acompanha o desempenho: os alunos de pior desempenho se dão 8,5. E o INDE do mesmo aluno fica estável, então hoje não dá para provar impacto além da defasagem.

**[2:50 a 3:15] Slide 10 · Modelo**

Para antecipar esses casos, treinamos um modelo que usa os indicadores de um ano para prever se a defasagem vai piorar no ano seguinte. Testado em 2023 para 2024, um ano que ele não viu, identificou 74% dos alunos que entraram em risco, sinalizando 23% da base.

**[3:15 a 3:35] Slide 11 · Comparação de modelos**

Testamos sete algoritmos. Os três baseados em árvores ficaram no topo, empatados dentro da margem de erro, e mantivemos o Random Forest, escolhido antes de olhar o teste. A vantagem sobre a regressão logística mostra que o risco depende de combinações de fatores.

**[3:35 a 4:00] Slide 12 · Como usar**

No teste, acompanhar os 20% de maior risco alcançou 70% dos casos, contra 20% de uma escolha ao acaso. Para 2025, o modelo sinaliza 377 alunos, por isso a lista deve ser usada como ranking, até o limite da capacidade da equipe.

**[4:00 a 4:20] Slide 13 · Aplicação**

*(Mostrar a tela do app.)* O modelo já está num app em Streamlit. A equipe informa quantos alunos consegue acompanhar e recebe a lista em ordem de prioridade, consulta um aluno ou envia o arquivo de uma turma.

**[4:20 a 4:35] Slide 14 · Recomendações**

Com os alunos: usar a lista no início do ano, tratar o psicossocial como alerta precoce e reforçar Português. Na medição: rever a autoavaliação, padronizar as escalas e registrar por que os alunos saem.

**[4:35 a 4:50] Slide 15 · Riscos**

O modelo acerta mais na ALFA do que nas fases 3 a 5, onde a lista deve ser somada à indicação dos educadores. E, sem grupo de controle, propomos medir o efeito comparando alunos atendidos e não atendidos.

**[4:50 a 5:00] Slide 16 · Próximos passos**

Adotar a lista de 2025, medir o efeito e retreinar o modelo com o PEDE 2025. Obrigado.

## Dicas de gravação

- Grave com a apresentação em tela cheia e a câmera no canto; o enunciado exige pelo menos uma pessoa do grupo aparecendo.
- Para o trecho do app, grave 15 segundos na aba "Lista de risco 2025", mudando a capacidade da equipe, e depois em "Consultar aluno", no app publicado.
- Treine uma vez com cronômetro. Se passar de 5 minutos, encurte primeiro a fala dos slides 4, 8 e 9, que podem ficar só com uma frase.
