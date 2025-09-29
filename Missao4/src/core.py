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
