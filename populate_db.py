import asyncio
from datetime import datetime, timedelta
from database import init_db, db_client
from models import User, Category, Account, Transaction
from dotenv import load_dotenv

load_dotenv()

async def populate_database():
    """Popula o banco de dados com dados realistas"""
    
    # Inicializar beanie e conecta ao mongoDB
    await init_db()
    
    # Limpa todas as coleções existentes
    await User.delete_all()
    await Category.delete_all()
    await Account.delete_all()
    await Transaction.delete_all()
    
    print(" Coleções limpas")
    
    # Criar usuários
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
    for user_data in users_data:
        user = User(
            nome=user_data["nome"],
            email=user_data["email"],
            senha_hash=f"{user_data['senha']}"
        )
        await user.create()
        users.append(user)
    
    print(f" {len(users)} usuários criados")
    
    # Cria categorias
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
    for i, cat_name in enumerate(categories_names):
        user = users[i % len(users)]  # Distribui categorias entre usuários
        category = Category(
            nome=cat_name,
            user=user  # referencia ao usuario
        )
        await category.create()
        categories.append(category)
    
    print(f" {len(categories)} categorias criadas")
    
    # Contas
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
    for i, acc_name in enumerate(account_names):
        user = users[i % len(users)]
        acc_type = account_types[i % len(account_types)]
        account = Account(
            nome=acc_name,
            tipo=acc_type,
            saldo_inicial=round(1000 + (i * 500), 2),
            usuario=user  # type: ignore
        )
        await account.create()
        accounts.append(account)
    
    print(f"✓ {len(accounts)} contas criadas")
    
    # Cria transações
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
    
    for i in range(30):  # Criar 30 transações
        account = accounts[i % len(accounts)]
        category = categories[i % len(categories)]
        trans_type = transaction_types[i % len(transaction_types)]
        
        # Valor maior para entrada e menor para saida 
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
    
    print(f"✓ {len(transactions)} transações criadas")
    
    print("\n" + "="*50)
    print("✓ BANCO DE DADOS POPULADO COM SUCESSO!")
    print("="*50)
    print(f"  Usuários:      {len(users)}")
    print(f"  Categorias:    {len(categories)}")
    print(f"  Contas:        {len(accounts)}")
    print(f"  Transações:    {len(transactions)}")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(populate_database())
