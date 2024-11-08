from .disk_usage import check_disk_usage

def is_disk_full(path="/", threshold=10):
    """
    Vérifier si l'espace disque restant est en dessous d'un certain seuil.

    Args:
        path (str): Le chemin du disque ou répertoire à vérifier (par défaut /)
        threshold (int): Le seuil, en pourcentage, en dessous duquel on considère que le disque est presque plein
    
    Returns:
        bool: `True` si l'espace libre est en dessous du seuil, sinon `False`

    Examples:
        >>> is_disk_full(path, 10)
        False # si le disque a plus de 10% d'espace libre
    """
    total, used, free = check_disk_usage(path)

    free_percent = (free / total) * 100

    return free_percent < threshold

def alert_if_disk_full(path="/", threshold=10):
    """
    Affiche un message si l'espace disque est insuffisant.

    Args:
        path (str): Le chemin du disque ou répertoire à vérifier (par défaut /)
        threshold (int): Le seuil servant pour l'alerte 

    Returns:
        ???

    Examples:
        >>> alert_if_disk_full("/", 20)
        False # si le disque a plus de 20% d'espace libre
    """
    if is_disk_full(path, threshold):
        print(f"Attention : L'espace disque sur {path} est inférieur à {threshold}% !")
    else:
        print(f"Espace disque suffisant sur {path}.")