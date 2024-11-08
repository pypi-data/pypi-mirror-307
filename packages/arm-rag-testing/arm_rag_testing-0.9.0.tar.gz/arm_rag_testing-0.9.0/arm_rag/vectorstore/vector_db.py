from .deeplake_db import Deeplake_DB
from .weaviate_db import Weaviate_DB


def get_vectorstore(db_type, wcd_url, wcd_api_key, name, k, search_type, weight, distance_metric):
    if db_type == 'weaviate':
        return Weaviate_DB(wcd_url, wcd_api_key, name, k, search_type, weight)
    elif db_type == 'deeplake':
        return Deeplake_DB(name, k, distance_metric)
    else:
        raise ValueError("Invalid db_type")
