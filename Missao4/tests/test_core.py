import pytest
from pydantic import ValidationError
from datetime import date
from src.core import Expense

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