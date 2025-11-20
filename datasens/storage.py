"""
Client MinIO pour le stockage S3-compatible
Upload/Download de fichiers et gestion de buckets
"""

from minio import Minio
from minio.error import S3Error
from pathlib import Path
from typing import Optional, List, Dict
import logging
import io
import time

from .config import get_minio_config

logger = logging.getLogger(__name__)


class MinIOClient:
    """
    Wrapper pour le client MinIO avec méthodes simplifiées.
    """
    
    def __init__(self, endpoint: Optional[str] = None, access_key: Optional[str] = None, 
                 secret_key: Optional[str] = None, bucket: Optional[str] = None):
        """
        Initialise le client MinIO.
        
        Args:
            endpoint: URL du serveur MinIO (ex: "localhost:9000" ou "http://localhost:9000")
            access_key: Clé d'accès MinIO
            secret_key: Clé secrète MinIO
            bucket: Nom du bucket par défaut
        """
        # Charger config si non fournie
        if not all([endpoint, access_key, secret_key, bucket]):
            config = get_minio_config()
            endpoint = endpoint or config['endpoint']
            access_key = access_key or config['access_key']
            secret_key = secret_key or config['secret_key']
            bucket = bucket or config['bucket']
        
        # Nettoyer l'endpoint (enlever http:// ou https://)
        endpoint = endpoint.replace("http://", "").replace("https://", "")
        # Enlever le trailing slash si présent
        endpoint = endpoint.rstrip("/")
        
        self.endpoint = endpoint
        self.bucket = bucket
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False  # HTTP pour dev local
        )
        
        # Créer bucket s'il n'existe pas
        self._ensure_bucket()
        logger.info(f"🪣 Client MinIO initialisé: {endpoint}/{bucket}")
    
    def _ensure_bucket(self):
        """Crée le bucket s'il n'existe pas."""
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
                logger.info(f"✅ Bucket créé: {self.bucket}")
        except S3Error as e:
            logger.error(f"❌ Erreur création bucket: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Teste la connexion MinIO.
        
        Returns:
            bool: True si connexion OK, False sinon
        """
        try:
            start_time = time.time()
            # Tester avec bucket_exists
            exists = self.client.bucket_exists(self.bucket)
            duration = time.time() - start_time
            
            if exists:
                logger.info(f"✅ Connexion MinIO OK: {self.endpoint}/{self.bucket} ({duration:.2f}s)")
                return True
            else:
                logger.warning(f"⚠️ Bucket {self.bucket} n'existe pas sur {self.endpoint}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Connexion MinIO échouée: {self.endpoint} - {e}")
            return False
    
    def upload_file(self, local_path: Path, object_name: str, content_type: str = "application/octet-stream") -> str:
        """
        Upload un fichier local vers MinIO.
        
        Args:
            local_path: Chemin du fichier local
            object_name: Nom de l'objet dans MinIO (ex: "kaggle/data_20251120.csv")
            content_type: Type MIME du fichier
            
        Returns:
            str: URI S3 de l'objet (s3://bucket/object_name)
        """
        try:
            local_path = Path(local_path)
            start_time = time.time()
            file_size = local_path.stat().st_size
            
            self.client.fput_object(
                self.bucket,
                object_name,
                str(local_path),
                content_type=content_type
            )
            
            duration = time.time() - start_time
            uri = f"s3://{self.bucket}/{object_name}"
            logger.info(f"☁️ Upload: {local_path.name} ({file_size/1024:.2f}KB) → {uri} ({duration:.2f}s)")
            return uri
            
        except S3Error as e:
            logger.error(f"❌ Erreur upload {local_path.name}: {e}")
            raise
    
    def upload_dataframe(self, df, object_name: str, file_format: str = "csv") -> str:
        """
        Upload un DataFrame pandas vers MinIO.
        
        Args:
            df: DataFrame pandas
            object_name: Nom de l'objet dans MinIO
            file_format: Format du fichier ("csv" ou "parquet")
            
        Returns:
            str: URI S3 de l'objet
        """
        try:
            start_time = time.time()
            # Convertir DataFrame en bytes
            buffer = io.BytesIO()
            if file_format == "csv":
                df.to_csv(buffer, index=False)
                content_type = "text/csv"
            elif file_format == "parquet":
                df.to_parquet(buffer, index=False)
                content_type = "application/octet-stream"
            else:
                raise ValueError(f"Format non supporté: {file_format}")
            
            buffer.seek(0)
            buffer_size = buffer.getbuffer().nbytes
            
            # Upload
            self.client.put_object(
                self.bucket,
                object_name,
                buffer,
                length=buffer_size,
                content_type=content_type
            )
            
            duration = time.time() - start_time
            uri = f"s3://{self.bucket}/{object_name}"
            logger.info(f"☁️ Upload DataFrame: {len(df)} lignes ({buffer_size/1024:.2f}KB) → {uri} ({duration:.2f}s)")
            return uri
            
        except S3Error as e:
            logger.error(f"❌ Erreur upload DataFrame: {e}")
            raise
    
    def download_file(self, object_name: str, local_path: Path) -> Path:
        """
        Télécharge un objet MinIO vers un fichier local.
        
        Args:
            object_name: Nom de l'objet dans MinIO
            local_path: Chemin du fichier local de destination
            
        Returns:
            Path: Chemin du fichier téléchargé
        """
        try:
            local_path = Path(local_path)
            local_path.parent.mkdir(parents=True, exist_ok=True)
            
            start_time = time.time()
            self.client.fget_object(self.bucket, object_name, str(local_path))
            duration = time.time() - start_time
            
            file_size = local_path.stat().st_size
            logger.info(f"⬇️ Download: {object_name} ({file_size/1024:.2f}KB) → {local_path} ({duration:.2f}s)")
            return local_path
            
        except S3Error as e:
            logger.error(f"❌ Erreur download {object_name}: {e}")
            raise
    
    def list_objects(self, prefix: str = "", recursive: bool = True) -> List[Dict[str, str]]:
        """
        Liste les objets dans le bucket.
        
        Args:
            prefix: Préfixe pour filtrer les objets (ex: "kaggle/")
            recursive: Lister récursivement
            
        Returns:
            List[Dict]: Liste d'objets avec keys: 'name', 'size', 'last_modified'
        """
        try:
            start_time = time.time()
            objects = self.client.list_objects(self.bucket, prefix=prefix, recursive=recursive)
            
            result = []
            for obj in objects:
                result.append({
                    'name': obj.object_name,
                    'size': obj.size,
                    'last_modified': obj.last_modified
                })
            
            duration = time.time() - start_time
            logger.info(f"📋 List: {len(result)} objets (prefix='{prefix}') ({duration:.2f}s)")
            return result
            
        except S3Error as e:
            logger.error(f"❌ Erreur listage (prefix='{prefix}'): {e}")
            raise
    
    def delete_object(self, object_name: str):
        """
        Supprime un objet du bucket.
        
        Args:
            object_name: Nom de l'objet à supprimer
        """
        try:
            self.client.remove_object(self.bucket, object_name)
            logger.info(f"🗑️ Objet supprimé: {object_name}")
        except S3Error as e:
            logger.error(f"❌ Erreur suppression: {e}")
            raise
    
    def object_exists(self, object_name: str) -> bool:
        """
        Vérifie si un objet existe dans le bucket.
        
        Args:
            object_name: Nom de l'objet
            
        Returns:
            bool: True si existe, False sinon
        """
        try:
            self.client.stat_object(self.bucket, object_name)
            return True
        except S3Error:
            return False
