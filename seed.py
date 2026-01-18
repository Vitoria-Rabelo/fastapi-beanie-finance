
"""
Script de seed para inserção de dados no MongoDB
Uso: python seed.py [--clean] [--seed] [--verbose]
"""

import asyncio
import argparse
from datetime import datetime, timedelta
from database import init_db
from models import User, Category, Account, Transaction
from dotenv import load_dotenv

load_dotenv()

#apaga todos os dados do banco 
async def clean_database():
    """Limpa todas as coleções do banco"""
    await init_db()
    print("Limpando coleções...")
    
    await User.delete_all()
    await Category.delete_all()
    await Account.delete_all()
    await Transaction.delete_all()
    
    print("Coleções limpas com sucesso\n")

#cria usuarios realistas
async def seed_users():
    """Insere usuários no banco"""
    users_data = [
        {"nome": "João Silva", "email": "joao@example.com", "senha": "senha123"},
        {"nome": "Maria Santos", "email": "maria@example.com", "senha": "senha123"},
        {"nome": "Pedro Oliveira", "email": "pedro@example.com", "senha": "senha123"},
        {"nome": "Ana Costa", "email": "ana@example.com", "senha": "senha123"},
        {"nome": "Carlos Ferreira", "email": "carlos@example.com", "senha": "senha123"},
        {"nome": "Lucia Mendes", "email": "lucia@example.com", "senha": "senha123"},
        {"nome": "Roberto Gomes", "email": "roberto@example.com", "senha": "senha123"},
        {"nome": "Fernanda Lima", "email": "fernanda@example.com", "senha": "senha123"},
        {"nome": "Rafael Souza", "email": "rafael@example.com", "senha": "senha123"},
        {"nome": "Camila Rocha", "email": "camila@example.com", "senha": "senha123"},
        {"nome": "Thiago Martins", "email": "thiago@example.com", "senha": "senha123"},
    ]
    
    users = []
    print("Inserindo usuários...")
    for user_data in users_data:
        user = User(
            nome=user_data["nome"],
            email=user_data["email"],
            senha_hash=f"{user_data['senha']}"
        )
        await user.create()
        users.append(user)
        print(f" {user_data['nome']}")
    
    print(f"\n{len(users)} usuários criados\n")
    return users

#Cria categorias vinculadas aos usuarios
async def seed_categories(users):
    """Insere categorias no banco"""
    categories_names = [
        "Alimentação",
        "Transporte",
        "Utilitários",
        "Educação",
        "Saúde",
        "Diversão",
        "Roupas",
        "Casa",
        "Tecnologia",
        "Seguros",
        "Viagem"
    ]
    
    categories = []
    print("Inserindo categorias...")
    for i, cat_name in enumerate(categories_names):
        user = users[i % len(users)]
        category = Category(
            nome=cat_name,
            user=user  # type: ignore
        )
        await category.create()
        categories.append(category)
        print(f"{cat_name}")
    
    print(f"\n {len(categories)} categorias criadas\n")
    return categories

#Cria contas bancárias ligadas a usuários
async def seed_accounts(users):
    """Insere contas no banco"""
    account_types = ["Conta corrente", "Conta poupança", "Cartão de crédito", "Conta de investimento"]
    account_names = [
        "Conta Principal",
        "Conta Salário",
        "Poupança Emergência",
        "Reserva de Viagem",
        "Nubank",
        "Banco do Brasil",
        "Caixa Econômica",
        "Itaú",
        "Bradesco",
        "Cartão Visa",
        "Cartão Mastercard"
    ]
    
    accounts = []
    print("Inserindo contas...")
    for i, acc_name in enumerate(account_names):
        user = users[i % len(users)]
        acc_type = account_types[i % len(account_types)]
        account = Account(
            nome=acc_name,
            tipo=acc_type,
            saldo_inicial=round(1000 + (i * 500), 2),
            usuario=user
        )
        await account.create()
        accounts.append(account)
        print(f"   {acc_name} ({acc_type}) - R$ {account.saldo_inicial}")
    
    print(f"\n {len(accounts)} contas criadas\n")
    return accounts

#Cria transações financeiras
async def seed_transactions(accounts, categories):
    """Insere transações no banco"""
    transaction_types = ["Entrada", "Saída", "Transferência"]
    transaction_descriptions = [
        "Salário",
        "Compra no supermercado",
        "Ônibus",
        "Conta de água",
        "Internet",
        "Cinema",
        "Compras online",
        "Almoço no restaurante",
        "Farmácia",
        "Combustível",
        "Matrícula escola",
        "Spa",
        "Passagem aérea",
        "Hotel",
        "Restaurante"
    ]
    
    transactions = []
    base_date = datetime.now() - timedelta(days=90)
    
    print("Inserindo transações...")
    for i in range(30):
        account = accounts[i % len(accounts)]
        category = categories[i % len(categories)]
        trans_type = transaction_types[i % len(transaction_types)]
        
        if trans_type == "Entrada":
            valor = round(2000 + (i * 100), 2)
        elif trans_type == "Saída":
            valor = round(50 + (i * 20), 2)
        else:
            valor = round(100 + (i * 50), 2)
        
        transaction = Transaction(
            descricao=transaction_descriptions[i % len(transaction_descriptions)],
            valor=valor,
            data=base_date + timedelta(days=i),
            tipo=trans_type,
            conta=account,  
            categoria=category  
        )
        await transaction.create()
        transactions.append(transaction)
        print(f"   {transaction_descriptions[i % len(transaction_descriptions)]} ({trans_type}) - R$ {valor}")
    
    print(f"\n {len(transactions)} transações criadas\n")
    return transactions

#Função principal de população do banco
async def seed_database():
    """Executa o seed completo do banco"""
    print("\n" + "="*60)
    print("INICIANDO SEED DO BANCO DE DADOS")
    print("="*60 + "\n")
    
    await init_db()
    
    users = await seed_users()
    categories = await seed_categories(users)
    accounts = await seed_accounts(users)
    transactions = await seed_transactions(accounts, categories)
    
    print("="*60)
    print(" SEED CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print(f" Usuários: {len(users)}")
    print(f" Categorias: {len(categories)}")
    print(f" Contas: {len(accounts)}")
    print(f" Transações: {len(transactions)}")
    print("="*60 + "\n")


async def main():
    parser = argparse.ArgumentParser(
        description="Script de seed para inserção de dados no MongoDB"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Limpar todas as coleções antes de fazer o seed"
    )
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Executar seed dos dados"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Modo verbose (mais detalhes)"
    )
    
    args = parser.parse_args()
    
    # Se nenhuma opção foi fornecida, executar clean + seed
    if not args.clean and not args.seed:
        args.clean = True
        args.seed = True
    
    if args.clean:
        await clean_database()
    
    if args.seed:
        await seed_database()


if __name__ == "__main__":
    asyncio.run(main())
