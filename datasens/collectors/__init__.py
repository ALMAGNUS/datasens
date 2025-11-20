"""
Collecteurs de données pour DataSens
"""

from .kaggle import collect_kaggle_csv
from .rss import collect_rss_feeds
from .owm import collect_weather_data
from .webscraping import collect_webscraping_multisources

__all__ = ['collect_kaggle_csv', 'collect_rss_feeds', 'collect_weather_data', 'collect_webscraping_multisources']
