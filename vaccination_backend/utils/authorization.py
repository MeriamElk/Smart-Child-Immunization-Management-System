def role_required(allowed_roles):
    """
    Décorateur pour restreindre l'accès à une fonction selon le rôle de l'utilisateur.
    Exemple : @role_required(["admin", "médecin"])
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            utilisateur = kwargs.get("utilisateur")
            if not utilisateur:
                raise PermissionError("❌ Utilisateur non authentifié.")
            if utilisateur.role not in allowed_roles:
                raise PermissionError(f"❌ Accès interdit pour le rôle : {utilisateur.role}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
