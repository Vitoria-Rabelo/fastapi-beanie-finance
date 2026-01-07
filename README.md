# fastapi-beanie-finance
API de Gestão Financeira e Controle de Gastos Assíncrona desenvolvida com FastAPI, MongoDB e Beanie ODM.

<h2>Tecnologias:</h2>
FastAPI para construção da API
Persistência de dados no MongoDB usando driver assíncrono.
Suporte para MongoDB como banco de dados NoSQL
UV como gerenciador de dependências
Benie como ODM compatível com o Pydantic

<h2>A API implementa</h2>
Consultas Requeridas: A API deve implementar consultas diversificadas e úteis ao contexto escolhido.

a) Consultas por ID
b) Listagens filtradas por relacionamentos
c) Buscas por texto parcial e case-insensitive.
d) Filtros por data/ano utilizando consultas baseadas em operadores do MongoDB
e) Agregações e contagens utilizando aggregation pipeline
f) Classificações e ordenações
g) Consultas complexas envolvendo múltiplas coleções

<h3>Preparando ambiente Mongo</h3>
1) Instale o MongoDB Compass (GUI)
2) Crie sua conta no MongoDB Atlas (versão gratuita que hospeda em nuvem)

<h3>Preparando seu projeto python 3.13</h3>
Repare que para esse projeto usamos UV como gerenciador de pacotes.
