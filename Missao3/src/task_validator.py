# src/task_validator.py

def validate_task(task: dict):
    """
    Valida uma tarefa de acordo com as regras de negócio.

    Args:
        task (dict): Um dicionário representando a tarefa.

    Returns:
        bool: True se a tarefa for válida.

    Raises:
        ValueError: Se a tarefa for inválida.
    """
    # Regra 1: Deve ter um título
    if "titulo" not in task:
        raise ValueError("A tarefa deve conter uma chave 'titulo'")

    # Regra 2: O título não pode ser vazio
    if not isinstance(task["titulo"], str) or not task["titulo"].strip():
        raise ValueError("O titulo da tarefa nao pode ser vazio")

    # Regra 3: Deve ter prioridade
    if "prioridade" not in task:
        raise ValueError("A tarefa deve conter uma chave 'prioridade'")

    # Regra 4: A prioridade deve ser válida
    valid_priorities = ["baixa", "media", "alta"]
    if task["prioridade"] not in valid_priorities:
        raise ValueError(f"Prioridade '{task['prioridade']}' invalida. Use uma de: {valid_priorities}")

    return True