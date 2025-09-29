import pytest
from pydantic import ValidationError
from datetime import date
from src.core import Expense, ExpenseRepository

def test_criar_despesa_valida():
    """Testa a criação de uma despesa com dados válidos."""
    expense = Expense(
        id=1,
        description="Café da manhã",
        amount=15.50,
        category="Alimentação",
        date=date(2025, 9, 21)
    )
    assert expense.id == 1
    assert expense.description == "Café da manhã"
    assert expense.amount == 15.50

def test_nao_criar_despesa_com_valor_negativo():
    """Testa que uma despesa não pode ser criada com valor negativo ou zero."""
    with pytest.raises(ValidationError) as excinfo:
        Expense(id=2, description="Invalido", amount=-100, category="Teste", date=date.today())
    # Verifica se a mensagem de erro da Pydantic informa sobre o valor
    assert "Input should be greater than 0" in str(excinfo.value)

def test_nao_criar_despesa_com_descricao_curta():
    """Testa que a descrição deve ter pelo menos 3 caracteres."""
    with pytest.raises(ValidationError):
        Expense(id=3, description="ab", amount=20, category="Teste", date=date.today())

def test_nao_criar_despesa_com_categoria_vazia():
    """Testa que a categoria não pode ser uma string vazia."""
    with pytest.raises(ValueError) as excinfo:
        Expense(id=4, description="Teste categoria", amount=50, category="   ", date=date.today())
    assert "A categoria não pode ser vazia" in str(excinfo.value)


@pytest.fixture
def repo():
    """Cria uma instância limpa do repositório para cada teste."""
    return ExpenseRepository()

def test_adicionar_despesa_ao_repositorio(repo):
    """Testa se uma despesa é adicionada corretamente e recebe um ID."""
    expense_data = {
        "description": "Almoço", "amount": 35.0, "category": "Alimentação", "date": date.today()
    }
    new_expense = repo.add(expense_data)
    
    assert new_expense.id == 1
    assert len(repo.get_all()) == 1
    assert repo.get_by_id(1) == new_expense

def test_buscar_despesa_por_id_existente(repo):
    """Testa a busca de uma despesa que existe."""
    expense_data = {"description": "Cinema", "amount": 50.0, "category": "Lazer", "date": date.today()}
    repo.add(expense_data)
    
    found_expense = repo.get_by_id(1)
    assert found_expense is not None
    assert found_expense.id == 1
    assert found_expense.description == "Cinema"

def test_buscar_despesa_por_id_inexistente(repo):
    """Testa a busca de uma despesa que não existe."""
    assert repo.get_by_id(999) is None

def test_adicionar_multiplas_despesas_incrementa_id(repo):
    """Testa se os IDs são auto-incrementados corretamente."""
    repo.add({"description": "Uber", "amount": 22.0, "category": "Transporte", "date": date.today()})
    repo.add({"description": "Livro", "amount": 80.0, "category": "Educação", "date": date.today()})
    
    despesa_2 = repo.get_by_id(2)
    assert len(repo.get_all()) == 2
    assert despesa_2 is not None
    assert despesa_2.description == "Livro"
