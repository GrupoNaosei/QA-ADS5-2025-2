import pytest
from pydantic import ValidationError
from datetime import date
from src.core import Expense, ExpenseRepository, FinancialManager

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
# ... (testes anteriores continuam aqui) ...
from src.core import FinancialManager

def test_financial_manager_adiciona_despesa(mocker):
    """Testa se o FinancialManager chama corretamente o método add do repositório."""
    # Cria um mock do repositório
    mock_repo = mocker.MagicMock(spec=ExpenseRepository)
    manager = FinancialManager(repository=mock_repo)
    
    expense_data = {"description": "Jantar", "amount": 120.0, "category": "Alimentação", "date": date.today()}
    manager.add_expense(expense_data)
    
    # Verifica se o método 'add' do mock foi chamado exatamente uma vez com os dados corretos
    mock_repo.add.assert_called_once_with(expense_data)

def test_get_total_expenses_com_varias_despesas(mocker):
    """Testa o cálculo do total de despesas, usando um repositório mockado."""
    mock_repo = mocker.MagicMock(spec=ExpenseRepository)
    # Configura o valor de retorno do mock
    mock_repo.get_all.return_value = [
        Expense(id=1, description="abc", amount=10.50, category="c", date=date.today()),
        Expense(id=2, description="bca", amount=20.00, category="c", date=date.today()),
        Expense(id=3, description="cba", amount=0.50, category="c", date=date.today()),
    ]
    
    manager = FinancialManager(repository=mock_repo)
    total = manager.get_total_expenses()
    
    assert total == 31.00

def test_get_total_expenses_sem_despesas(mocker):
    """Testa o cálculo do total quando não há despesas."""
    mock_repo = mocker.MagicMock(spec=ExpenseRepository)
    mock_repo.get_all.return_value = [] # Retorna uma lista vazia
    
    manager = FinancialManager(repository=mock_repo)
    total = manager.get_total_expenses()
    
    assert total == 0.0

@pytest.mark.parametrize(
    "amount, expected_category",
    [
        (15.0, "Baixo"),     # Teste 1: Custo baixo
        (20.0, "Baixo"),     # Teste 2: Custo baixo (limite)
        (20.01, "Médio"),    # Teste 3: Custo médio (acima do limite)
        (100.0, "Médio"),    # Teste 4: Custo médio (limite)
        (100.01, "Alto"),    # Teste 5: Custo alto (acima do limite)
        (5000.0, "Alto"),    # Teste 6: Custo alto
    ]
)
def test_categorize_expense_by_cost(amount, expected_category):
    """Testa a categorização por custo com diferentes valores."""
    manager = FinancialManager(repository=None) # Não precisamos de repo aqui
    expense = Expense(id=1, description="Teste", amount=amount, category="cat", date=date.today())
    
    result = manager.categorize_expense_by_cost(expense)
    
    assert result == expected_category
