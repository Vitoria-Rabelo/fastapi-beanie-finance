# Scripts de Seed - FastAPI Beanie Finance

## Descrição
Scripts para popular o banco de dados MongoDB com dados realistas para desenvolvimento e testes.

## Arquivos de Seed

### 1. `seed.py` (Recomendado)
Script principal com opções de linha de comando para mais controle.

**Uso:**
```bash
python seed.py # Executar limpeza + seed (padrão)
python seed.py --seed # Apenas fazer seed (sem limpar)
python seed.py --clean # Apenas limpar (sem inserir dados)
python seed.py -v # Com modo verbose (mais detalhes)
```

### 2. `populate_db.py`
Script simples e direto que limpa e popula o banco automaticamente.

**Uso:**
```bash
python populate_db.py
```

## Dados Inseridos

### Usuários (11 registros)
- João Silva
- Maria Santos
- Pedro Oliveira
- Ana Costa
- Carlos Ferreira
- Lucia Mendes
- Roberto Gomes
- Fernanda Lima
- Rafael Souza
- Camila Rocha
- Thiago Martins

### Categorias (11 registros)
- Alimentação
- Transporte
- Utilitários
- Educação
- Saúde
- Diversão
- Roupas
- Casa
- Tecnologia
- Seguros
- Viagem

### Contas (11 registros)
Tipos:
- Conta corrente
- Conta poupança
- Cartão de crédito
- Conta de investimento

Nomes: Vinculados aos usuários

### Transações (30 registros)
- Tipos: Entrada, Saída, Transferência
- Datas: Distribuídas nos últimos 90 dias
- Valores: Variados de acordo com o tipo

## Relacionamentos

Todos os relacionamentos estão corretamente vinculados:
- **Usuários → Categorias** (1:N)
- **Usuários → Contas** (1:N)
- **Contas ↔ Transações** (1:N)
- **Categorias ↔ Transações** (1:N)

## Verificação

```bash
# Listar usuários
curl http://localhost:8000/users/

# Listar categorias
curl http://localhost:8000/categories/

# Listar contas
curl http://localhost:8000/accounts/

# Listar transações
curl http://localhost:8000/transactions/
```

Ou acesse a documentação interativa em: **http://localhost:8000/docs**

## Requisitos
- MongoDB rodando em `localhost:27017`
- Environment `.env` configurado corretamente
- Dependências instaladas: `uv sync`

## Notas
- O seed limpa todas as coleções antes de inserir dados
- Os dados são gerados de forma determinística (sempre os mesmos dados)
- Ideal para ambiente de desenvolvimento e testes
- **NÃO usar em produção**
