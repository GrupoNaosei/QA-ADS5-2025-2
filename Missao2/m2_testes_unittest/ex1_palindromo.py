"""import unicodedata

def is_palindrome(text: str) -> bool:
    """
    Verifica se 'text' é palíndromo desconsiderando:
    - diferenças de maiúsculas/minúsculas (casefold)
    - acentos (normalização Unicode)
    - espaços e pontuação (mantém apenas caracteres alfanuméricos)
    Levanta ValueError se text for None.
    """
    if text is None:
        raise ValueError("text não pode ser None")

    # Normaliza (NFD) e remove diacríticos (acentos)
    normalized = unicodedata.normalize("NFD", text)
    sem_acentos = "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")
    # Mantém apenas alfanuméricos e aplica casefold
    filtrado = "".join(ch for ch in sem_acentos if ch.isalnum()).casefold()
    return filtrado == filtrado[::-1]
    """