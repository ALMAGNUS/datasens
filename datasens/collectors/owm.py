"""
Collecteur OpenWeatherMap
API météo en temps réel
"""

import pandas as pd
import requests
from pathlib import Path
from typing import List, Tuple, Optional
import logging
from sqlalchemy import text
from tqdm import tqdm

from ..config import RAW_DIR
from ..storage import MinIOClient
from ..utils import ts
from ..retry import retry_on_network_error

logger = logging.getLogger(__name__)


def _get_source_id(conn, nom: str) -> Optional[int]:
    """Récupère l'ID d'une source depuis t02_source"""
    result = conn.execute(
        text("SELECT id_source FROM datasens.t02_source WHERE nom = :nom"), 
        {"nom": nom}
    ).scalar()
    return result


def _create_flux(conn, source_nom: str, format_type: str = "json", manifest_uri: str = None) -> int:
    """Crée un flux dans t03_flux"""
    sid = _get_source_id(conn, source_nom)
    if not sid:
        # Créer la source si elle n'existe pas
        tid = conn.execute(text("SELECT id_type_donnee FROM datasens.t01_type_donnee WHERE libelle = 'api_weather' LIMIT 1")).scalar()
        if not tid:
            tid = 1  # Fallback
        sid = conn.execute(text("""
            INSERT INTO datasens.t02_source(id_type_donnee, nom, url, fiabilite) 
            VALUES (:tid, :nom, 'https://openweathermap.org', 0.9) RETURNING id_source
        """), {"tid": tid, "nom": source_nom}).scalar()
    
    return conn.execute(text("""
        INSERT INTO datasens.t03_flux(id_source, format, manifest_uri, date_collecte)
        VALUES (:sid, :format, :manifest, NOW()) RETURNING id_flux
    """), {"sid": sid, "format": format_type, "manifest": manifest_uri}).scalar()


def _ensure_territoire_complet(conn, ville: str, lat: float = None, lon: float = None) -> int:
    """Crée ou récupère territoire avec hiérarchie t13-t17"""
    # Chercher commune existante par nom
    commune_id = conn.execute(text("""
        SELECT id_commune FROM datasens.t16_commune WHERE nom_commune = :ville
    """), {"ville": ville}).scalar()
    
    if commune_id:
        # Récupérer territoire existant
        terr_id = conn.execute(text("""
            SELECT id_territoire FROM datasens.t17_territoire WHERE id_commune = :c
        """), {"c": commune_id}).scalar()
        if terr_id:
            return terr_id
    
    # Créer hiérarchie minimale si nécessaire
    # 1. Pays France
    pays_id = conn.execute(text("SELECT id_pays FROM datasens.t13_pays WHERE nom = 'France' LIMIT 1")).scalar()
    if not pays_id:
        pays_id = conn.execute(text("INSERT INTO datasens.t13_pays(nom) VALUES ('France') RETURNING id_pays")).scalar()
    
    # 2. Région par défaut
    region_id = conn.execute(text("SELECT id_region FROM datasens.t14_region WHERE nom = 'Région par défaut' LIMIT 1")).scalar()
    if not region_id:
        region_id = conn.execute(text("""
            INSERT INTO datasens.t14_region(id_pays, nom) 
            VALUES (:p, 'Région par défaut') RETURNING id_region
        """), {"p": pays_id}).scalar()
    
    # 3. Département par défaut
    dept_id = conn.execute(text("SELECT id_departement FROM datasens.t15_departement WHERE code_dept = '00' LIMIT 1")).scalar()
    if not dept_id:
        dept_id = conn.execute(text("""
            INSERT INTO datasens.t15_departement(id_region, code_dept, nom) 
            VALUES (:r, '00', 'Département par défaut') RETURNING id_departement
        """), {"r": region_id}).scalar()
    
    # 4. Créer commune si inexistante
    if not commune_id:
        import hashlib
        code_insee = f"99{hashlib.md5(ville.encode()).hexdigest()[:3]}"
        try:
            commune_id = conn.execute(text("""
                INSERT INTO datasens.t16_commune(id_departement, code_insee, nom_commune, lat, lon) 
                VALUES (:d, :code, :ville, :lat, :lon) 
                ON CONFLICT (code_insee) DO UPDATE SET nom_commune = EXCLUDED.nom_commune
                RETURNING id_commune
            """), {"d": dept_id, "code": code_insee, "ville": ville, "lat": lat, "lon": lon}).scalar()
        except:
            commune_id = conn.execute(text("""
                SELECT id_commune FROM datasens.t16_commune WHERE nom_commune = :ville LIMIT 1
            """), {"ville": ville}).scalar()
    
    # 5. Créer territoire
    terr_id = conn.execute(text("""
        SELECT id_territoire FROM datasens.t17_territoire WHERE id_commune = :c
    """), {"c": commune_id}).scalar()
    
    if not terr_id:
        terr_id = conn.execute(text("""
            INSERT INTO datasens.t17_territoire(id_commune) 
            VALUES (:c) RETURNING id_territoire
        """), {"c": commune_id}).scalar()
    
    return terr_id


def collect_weather_data(
    cities: List[str],
    api_key: str,
    source_name: str = "OpenWeatherMap",
    engine = None
) -> Tuple[int, str, pd.DataFrame]:
    """
    Collecte données météo depuis OpenWeatherMap API.
    
    Args:
        cities: Liste des villes (format "Paris,FR")
        api_key: Clé API OpenWeatherMap
        source_name: Nom de la source dans t02_source
        engine: SQLAlchemy engine (optionnel)
        
    Returns:
        Tuple[int, str, DataFrame]: (nb_relevés, minio_uri, dataframe)
    """
    logger.info(f"🌦️ Collecte OWM: {len(cities)} villes")
    
    if not api_key:
        logger.error("❌ API Key manquante")
        return 0, "", pd.DataFrame()
    
    @retry_on_network_error(max_retries=3)
    def fetch_weather(city: str) -> dict:
        """Récupère météo avec retry automatique"""
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": api_key, "units": "metric", "lang": "fr"},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    rows = []
    for city in tqdm(cities, desc="OWM"):
        try:
            data = fetch_weather(city)
            rows.append({
                "ville": data["name"],
                "lat": data["coord"]["lat"],
                "lon": data["coord"]["lon"],
                "date_obs": pd.to_datetime(data["dt"], unit="s"),
                "temperature": data["main"]["temp"],
                "humidite": data["main"]["humidity"],
                "vent_kmh": (data.get("wind", {}).get("speed") or 0) * 3.6,
                "pression": data.get("main", {}).get("pressure"),
                "meteo_type": data["weather"][0]["main"] if data.get("weather") else ""
            })
            logger.info(f"✅ {data['name']}: {data['main']['temp']}°C")
        except Exception as e:
            logger.error(f"❌ {city}: {str(e)[:80]}")
    
    if len(rows) == 0:
        logger.warning("⚠️ Aucun relevé météo collecté")
        return 0, "", pd.DataFrame()
    
    df = pd.DataFrame(rows)
    logger.info(f"📊 Total: {len(df)} relevés")
    
    # Sauvegarde locale
    local_path = RAW_DIR / "api" / "owm" / f"owm_{ts()}.csv"
    local_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(local_path, index=False)
    
    # Upload MinIO
    try:
        minio_client = MinIOClient()
        minio_uri = minio_client.upload_file(local_path, f"api/owm/{local_path.name}")
        logger.info(f"☁️ MinIO: {minio_uri}")
    except Exception as e:
        logger.warning(f"⚠️ MinIO upload échoué: {e}")
        minio_uri = f"local://{local_path}"
    
    # Insertion PostgreSQL
    if engine is None:
        from ..db import get_engine
        engine = get_engine()
    
    with engine.begin() as conn:
        conn.execute(text("SET search_path TO datasens, public"))
        
        # Créer flux
        flux_id = _create_flux(conn, source_name, "json", minio_uri)
        
        # Insérer dans t19_meteo avec territoires
        for _, row in df.iterrows():
            terr_id = _ensure_territoire_complet(conn, row["ville"], lat=row["lat"], lon=row["lon"])
            
            if terr_id:
                conn.execute(text("""
                    INSERT INTO datasens.t19_meteo(id_territoire, date_obs, temperature, humidite, vent_kmh, pression)
                    VALUES(:t, :d, :T, :H, :V, :P)
                """), {
                    "t": terr_id, 
                    "d": row["date_obs"], 
                    "T": row["temperature"],
                    "H": row["humidite"], 
                    "V": row["vent_kmh"], 
                    "P": row["pression"]
                })
    
    logger.info(f"✅ OWM: {len(df)} relevés insérés dans t19_meteo")
    return len(df), minio_uri, df
