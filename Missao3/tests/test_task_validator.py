# tests/test_task_validator.py

import pytest
from src.task_validator import validate_task

# Cenário 1: Teste de sucesso com uma tarefa perfeitamente válida
def test_validate_task_com_dados_validos():
    """Verifica se a validação retorna True para uma tarefa válida."""
    tarefa_valida = {"titulo": "  Aprender Pytest  ", "prioridade": "alta"}
    assert validate_task(tarefa_valida) is True

# Cenário 2: Teste de falha quando o título está faltando
def test_validate_task_sem_titulo():
    """Verifica se um ValueError é lançado quando a chave 'titulo' está ausente."""
    tarefa_invalida = {"prioridade": "media"}
    with pytest.raises(ValueError) as excinfo:
        validate_task(tarefa_invalida)
    # Verifica se a mensagem de erro contém o texto esperado
    assert "deve conter uma chave 'titulo'" in str(excinfo.value)

# Cenário 3: Teste de falha quando o título está vazio
def test_validate_task_com_titulo_vazio():
    """Verifica se um ValueError é lançado para um título vazio ou apenas com espaços."""
    tarefa_invalida = {"prioridade": "baixa"}
    with pytest.raises(ValueError) as excinfo:
        validate_task(tarefa_invalida)
    assert "titulo da tarefa nao pode ser vazio" in str(excinfo.value)

# Cenário 4: Teste de falha quando a prioridade está faltando
def test_validate_task_sem_prioridade():
    """Verifica se um ValueError é lançado quando a chave 'prioridade' está ausente."""
    tarefa_invalida = {"titulo": "Fazer o exercicio"}
    with pytest.raises(ValueError) as excinfo:
        validate_task(tarefa_invalida)
    assert "deve conter uma chave 'prioridade'" in str(excinfo.value)

# Cenário 5: Teste de falha com uma prioridade inválida
def test_validate_task_com_prioridade_invalida():
    """Verifica se um ValueError é lançado para uma prioridade inválida."""
    tarefa_invalida = {"titulo": "Corrigir o bug", "prioridade": "urgente"}
    with pytest.raises(ValueError) as excinfo:
        validate_task(tarefa_invalida)
    assert "Prioridade 'urgente' invalida" in str(excinfo.value)



"""
***Explicação:
*   **`import pytest`**: Importamos a biblioteca Pytest.
*   **`from src.task_validator import validate_task`**: Importamos nossa função a ser testada.
*   **`def test_...():`**: O Pytest automaticamente descobre funções que começam com `test_` como sendo testes.
*   **`assert`**: Usamos a palavra-chave `assert` para verificar se uma condição é verdadeira. Se for falsa, o teste falha.
*   **`with pytest.raises(ValueError):`**: Este é um recurso poderoso do Pytest. Ele diz: "Eu espero que o código dentro deste bloco `with` lance uma exceção do tipo `ValueError`". O teste passará se a exceção ocorrer, e falhará se não ocorrer.
*   **`as excinfo`**: Capturamos os detalhes da exceção para poder inspecionar a mensagem de erro, garantindo que ela seja informativa.

---

### **Passo 2: Executar os Testes Localmente**

Antes de automatizar, vamos garantir que tudo funciona na máquina.

**1. Instale o Pytest**
AbrA o terminal, navegar até a pasta raiz `projeto_de_testes/` e instalar o Pytest:

bash
pip install pytest
"""