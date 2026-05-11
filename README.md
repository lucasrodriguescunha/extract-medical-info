Profissionais de saúde costumam resumir os atendimentos em transcrições escritas em linguagem natural, que incluem detalhes sobre sintomas, diagnóstico e tratamentos. Essas transcrições podem ser usadas em outras documentações médicas, como para fins de seguro. No entanto, por conterem muitas informações clínicas, extrair com precisão os dados essenciais pode ser desafiador.

Você e sua equipe na Lakeside Healthcare Network decidiram usar a API da OpenAI para extrair automaticamente informações médicas dessas transcrições e automatizar o mapeamento para os códigos ICD-10 correspondentes. Os códigos ICD-10 são um sistema padronizado utilizado mundialmente para diagnóstico e faturamento, como no processamento de solicitações de seguro.

The Data
O conjunto de dados contém transcrições médicas anonimizadas, categorizadas por especialidade.

transcriptions.csv
Column	Description
"medical_specialty"	A especialidade médica associada a cada transcrição.
"transcription"	Textos detalhados de transcrição médica, com insights sobre o caso clínico.