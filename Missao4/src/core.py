from pydantic import BaseModel, Field, validator
from datetime import date

class Expense(BaseModel):
    """Representa uma única despesa."""
    id: int
    description: str = Field(min_length=3)
    amount: float = Field(gt=0) # gt=0 significa 'greater than 0'
    category: str
    date: date

    @validator('category')
    def category_must_be_valid(cls, v):
        """Valida se a categoria não está vazia."""
        if not v.strip():
            raise ValueError("A categoria não pode ser vazia")
        return v
#sim
class ExpenseRepository:
    """Gerencia uma coleção de despesas em memória."""
    def __init__(self):
        self._expenses: list[Expense] = []
        self._next_id: int = 1

    def add(self, expense_data: dict) -> Expense:
        """Adiciona uma nova despesa ao repositório."""
        # Cria uma instância do modelo Expense, que já valida os dados
        new_expense = Expense(id=self._next_id, **expense_data)
        self._expenses.append(new_expense)
        self._next_id += 1
        return new_expense

    def get_by_id(self, expense_id: int) -> Expense | None:
        """Busca uma despesa pelo seu ID."""
        for expense in self._expenses:
            if expense.id == expense_id:
                return expense
        return None

    def get_all(self) -> list[Expense]:
        """Retorna todas as despesas."""
        return self._expenses

# ... (classes Expense e ExpenseRepository continuam aqui) ...
class FinancialManager:
    """Gerencia as operações financeiras, usando um repositório."""
    def __init__(self, repository: ExpenseRepository):
        self._repository = repository

    def add_expense(self, expense_data: dict) -> Expense:
        """Adiciona uma nova despesa através do repositório."""
        # Delega a criação e armazenamento para o repositório
        return self._repository.add(expense_data)

    def get_total_expenses(self) -> float:
        """Calcula o valor total de todas as despesas."""
        all_expenses = self._repository.get_all()
        return sum(expense.amount for expense in all_expenses)

    def categorize_expense_by_cost(self, expense: Expense) -> str:
        """Categoriza uma despesa como 'Baixo', 'Médio' ou 'Alto' custo."""
        if expense.amount <= 20.0:
            return "Baixo"
        elif 20.0 < expense.amount <= 100.0:
            return "Médio"
        else:
            return "Alto"

import requests

def get_expense_in_usd(expense: Expense) -> float | None:
    """
    Converte o valor de uma despesa para USD usando uma API externa.
    A API fictícia é: https://api.exchangerate-api.com/v4/latest/BRL
    """
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/BRL")
        response.raise_for_status()  # Lança uma exceção para erros HTTP (4xx ou 5xx)
        
        data = response.json()
        usd_rate = data["rates"]["USD"]
        
        return round(expense.amount * usd_rate, 2)
    except requests.exceptions.RequestException:
        return None
    except (KeyError, TypeError):
        return None # Caso a resposta da API venha em um formato inesperado