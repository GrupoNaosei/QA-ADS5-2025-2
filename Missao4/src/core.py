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
