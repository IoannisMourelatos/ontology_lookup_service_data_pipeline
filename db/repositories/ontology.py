import concurrent.futures
import logging

from api.adapters.ols_api_data_provider import OlsApiDataProvider
from db.repositories.base import BaseRepository
from models.ontology import OlsApiResourceResponse, TermRetrieve

logger = logging.getLogger(__name__)

INSERT_OR_UPDATE_TERM_QUERY = """
    INSERT INTO terms (iri, label, parent_link, mesh_xref)
    VALUES (:iri, :label, :parent_link, :mesh_xref)
    ON CONFLICT (iri) DO UPDATE
    SET iri = EXCLUDED.iri,
        label = EXCLUDED.label,
        parent_link = EXCLUDED.parent_link,
        mesh_xref = EXCLUDED.mesh_xref
    RETURNING id, iri, label, parent_link, mesh_xref
"""

INSERT_OR_UPDATE_TERM_SYNONYM_QUERY = """
    INSERT INTO term_synonyms (synonym)
    VALUES (:synonym)
    ON CONFLICT (synonym) DO NOTHING
    RETURNING id, synonym
"""

INSERT_TERM_SYNONYM_RELATIONSHIP_QUERY = """
    INSERT INTO term_synonym_relationships (term_id, synonym_id)
    SELECT terms.id, term_synonyms.id
    FROM terms, term_synonyms
    WHERE terms.iri = :iri and term_synonyms.synonym = :synonym
    ON CONFLICT (term_id, synonym_id) DO NOTHING
    RETURNING id, term_id, synonym_id
"""

DELETE_TERM_SYNONYM_RELATIONSHIP_QUERY = """
    DELETE FROM term_synonym_relationships
    USING terms
    WHERE terms.id = term_synonym_relationships.term_id AND terms.iri = :iri
    RETURNING term_synonym_relationships.id, term_synonym_relationships.term_id, term_synonym_relationships.synonym_id;
"""


class OntologyRepository(BaseRepository):

    async def retrieve_all_terms(self):
        ols_api_data_provider = OlsApiDataProvider()
        ols_futures = list()
        batch_info = OlsApiResourceResponse.from_api_response(ols_api_data_provider.get_list_of_ontology_terms(0))
        pages = [*range(batch_info.current_page + 1, batch_info.total_pages + 1, 1)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for page in pages:
                ols_futures.append(executor.submit(ols_api_data_provider.get_list_of_ontology_terms, page))
        ols_results = list()
        for future in ols_futures:
            ols_results.append(future.result())
        results = sum([OlsApiResourceResponse.from_api_response(result) for result in ols_results] + [batch_info])
        # Try to insert terms - if already existing then update the information using the same query
        terms = await self.db.execute_many(
            query=INSERT_OR_UPDATE_TERM_QUERY,
            values=results.get_list_of_terms_for_database_operation()
        )
        # Try to insert synonyms - if already existing then update the information using the same query
        synonyms = await self.db.execute_many(
            query=INSERT_OR_UPDATE_TERM_SYNONYM_QUERY,
            values=results.get_list_of_unique_synonyms_for_database_operation()
        )
        # If updating terms we need to delete relevant relationships and recreate, in case something has changed
        # If inserting new terms the delete statement will of course not find any relationships to drop
        deleted_relationships = await self.db.execute_many(
            query=DELETE_TERM_SYNONYM_RELATIONSHIP_QUERY,
            values=results.get_list_of_iri_values_for_database_operation()
        )
        relationships = await self.db.execute_many(
            query=INSERT_TERM_SYNONYM_RELATIONSHIP_QUERY,
            values=results.get_list_of_unique_term_and_synonym_relationship_combinations_for_database_operation()
        )
        return terms, synonyms, deleted_relationships, relationships

    async def retrieve_terms(self, *, terms_to_retrieve: TermRetrieve):
        ols_api_data_provider = OlsApiDataProvider()
        query_values = terms_to_retrieve.dict().get('iri')
        ols_futures = list()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for term in query_values:
                ols_futures.append(executor.submit(ols_api_data_provider.get_ontology_term, term))
        ols_results = list()
        for future in ols_futures:
            ols_results.append(future.result())
        results = OlsApiResourceResponse.from_list(ols_results)
        # Try to insert terms - if already existing then update the information using the same query
        terms = await self.db.execute_many(
            query=INSERT_OR_UPDATE_TERM_QUERY,
            values=results.get_list_of_terms_for_database_operation()
        )
        # Try to insert synonyms - if already existing then update the information using the same query
        synonyms = await self.db.execute_many(
            query=INSERT_OR_UPDATE_TERM_SYNONYM_QUERY,
            values=results.get_list_of_unique_synonyms_for_database_operation()
        )
        # If updating terms we need to delete relevant relationships and recreate, in case something has changed
        # If inserting new terms the delete statement will of course not find any relationships to drop
        deleted_relationships = await self.db.execute_many(
            query=DELETE_TERM_SYNONYM_RELATIONSHIP_QUERY,
            values=results.get_list_of_iri_values_for_database_operation()
        )
        relationships = await self.db.execute_many(
            query=INSERT_TERM_SYNONYM_RELATIONSHIP_QUERY,
            values=results.get_list_of_unique_term_and_synonym_relationship_combinations_for_database_operation()
        )
        return terms, synonyms, deleted_relationships, relationships
