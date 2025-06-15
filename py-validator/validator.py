import re

def is_valid_product_slug(slug: str) -> bool:
    """
    Valida se o slug de um produto segue o padrão da empresa (ex: 'produto-incrivel-a1b2').
    Padrão: letras minúsculas, hífens e um código alfanumérico no final.
    """
    pattern = r"^[a-z0-9]+(?:-[a-z0-9]+)*-[a-z0-9]{4}$"
    return bool(re.match(pattern, slug))