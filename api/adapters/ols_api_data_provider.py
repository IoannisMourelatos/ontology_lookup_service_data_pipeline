import logging
import requests

from core.config import DEFAULT_ONTOLOGY, OLS_API_URL, OLS_API_MAX_ITEMS_PER_REQUEST
from utils import double_url_encode

logger = logging.getLogger(__name__)


class OlsApiDataProvider(object):
    def __init__(self):
        self.url = OLS_API_URL

    def get_list_of_ontology_terms(self, page: int):
        try:
            url = f'{self.url}/{DEFAULT_ONTOLOGY}/terms?size={OLS_API_MAX_ITEMS_PER_REQUEST}&page={page}'
            return requests.request('GET', url).json()
        except Exception as exception:
            logger.error(exception)
            raise

    def get_ontology_term(self, iri: str):
        try:
            url = f'{self.url}/{DEFAULT_ONTOLOGY}/terms/{double_url_encode(iri)}'
            return requests.request('GET', url).json()
        except Exception as exception:
            logger.error(exception)
            raise
