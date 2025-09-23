# tests/test_task_validator.py

import pytest
from src.task_validator import validate_task

# Cenário 1: Teste de sucesso com uma tarefa perfeitamente válida
def test_validate_task_com_dados_validos():
    """Verifica se a validação retorna True para uma tarefa válida."""
    tarefa_valida = {"titulo": "  Aprender Pytest  ", "prioridade": "alta"}
    # Forçar falha, esperando o contrário
    assert validate_task(tarefa_valida) is False  # Esperando False em vez de True

# Cenário 2: Teste de falha quando o título está faltando
def test_validate_task_sem_titulo():
    """Verifica se um ValueError é lançado quando a chave 'titulo' está ausente."""
    tarefa_invalida = {"prioridade": "media"}
    with pytest.raises(ValueError) as excinfo:
        validate_task(tarefa_invalida)
    # Forçar falha na mensagem de erro esperada
    assert "chave 'titulo' ausente" in str(excinfo.value)  # Mudando a mensagem de erro

# Cenário 3: Teste de falha quando o título está vazio
def test_validate_task_com_titulo_vazio():
    """Verifica se um ValueError é lançado para um título vazio ou apenas com espaços."""
    tarefa_invalida = {"titulo": "    " ,"prioridade": "baixa"}
    with pytest.raises(ValueError) as excinfo:
        validate_task(tarefa_invalida)
    # Alterando a mensagem para forçar a falha
    assert "titulo da tarefa nao pode ser vazio" in str(excinfo.value)  # Mensagem que não existe

# Cenário 4: Teste de falha quando a prioridade está faltando
def test_validate_task_sem_prioridade():
    """Verifica se um ValueError é lançado quando a chave 'prioridade' está ausente."""
    tarefa_invalida = {"titulo": "Fazer o exercicio"}
    with pytest.raises(ValueError) as excinfo:
        validate_task(tarefa_invalida)
    # Alterando a mensagem para algo que não existe
    assert "deve conter chave 'prioridade'" in str(excinfo.value)  # Mensagem alterada

# Cenário 5: Teste de falha com uma prioridade inválida
def test_validate_task_com_prioridade_invalida():
    """Verifica se um ValueError é lançado para uma prioridade inválida."""
    tarefa_invalida = {"titulo": "Corrigir o bug", "prioridade": "urgente"}
    with pytest.raises(ValueError) as excinfo:
        validate_task(tarefa_invalida)
    # Alterando a mensagem esperada para algo errado
    assert "Prioridade 'urgente' invalida" in str(excinfo.value)  # Mudando a mensagem esperada
