import shutil
def check_disk_usage(path="/"):
    """
    Vérifier l'espace disque disponible sur un chemin spécifié en argument

    Args:
        path (str): Le chemin du répertoire disque à vérifier

    Returns:
        tuple: Un tuple contenant trois valeurs en octets:
            - total (int): l'espace disque total du chemin spécifié
            - used (int): l'espace disque déjà utilisé
            - free (int): l'espace disque encore disponible

    Examples:
        >>> total, used, free = check_disk_usage("/")
        >>> print(f"Total: {total} octets, Utilisé: {used} octets, Libre: {free} octets)
    """
    total, used, free = shutil.disk_usage(path)
    return total, used, free