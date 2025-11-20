"""
Utilitaires réutilisables pour DataSens
Hash, timestamps, gestion de fichiers
"""

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def sha256_hash(text: str) -> str:
    """
    Génère un hash SHA256 d'un texte.
    
    Args:
        text: Texte à hasher
        
    Returns:
        str: Hash SHA256 en hexadécimal
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def ts() -> str:
    """
    Génère un timestamp UTC au format ISO 8601.
    
    Format: YYYYMMDDTHHMMSSZ
    Exemple: 20251120T123045Z
    
    Returns:
        str: Timestamp UTC
    """
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def ensure_directory(path: Path, parents: bool = True, exist_ok: bool = True) -> Path:
    """
    Crée un répertoire s'il n'existe pas.
    
    Args:
        path: Chemin du répertoire
        parents: Créer les parents si nécessaire
        exist_ok: Ne pas lever d'erreur si existe déjà
        
    Returns:
        Path: Chemin du répertoire créé
    """
    path = Path(path)
    path.mkdir(parents=parents, exist_ok=exist_ok)
    logger.debug(f"📁 Répertoire assuré: {path}")
    return path


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Nettoie un nom de fichier pour le rendre valide.
    
    Args:
        filename: Nom de fichier original
        max_length: Longueur maximale
        
    Returns:
        str: Nom de fichier nettoyé
    """
    # Remplacer caractères invalides
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limiter la longueur
    if len(filename) > max_length:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        max_name_length = max_length - len(ext) - 1
        filename = name[:max_name_length] + ('.' + ext if ext else '')
    
    return filename


def format_bytes(bytes_count: int) -> str:
    """
    Formate un nombre d'octets en format lisible (KB, MB, GB).
    
    Args:
        bytes_count: Nombre d'octets
        
    Returns:
        str: Taille formatée
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.2f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.2f} PB"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Tronque un texte à une longueur maximale.
    
    Args:
        text: Texte à tronquer
        max_length: Longueur maximale
        suffix: Suffixe à ajouter si tronqué
        
    Returns:
        str: Texte tronqué
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
