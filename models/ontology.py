from itertools import chain, product
from typing import Optional, List

from core.config import MESH_DB_URL
from models.core import IDModelMixin, CoreModel


class OlsApiOntologyResponse(CoreModel):
    iri: str
    label: Optional[str]
    synonyms: List[str]
    parent_link: Optional[str]
    mesh_xref: Optional[str]

    @classmethod
    def from_embedded_term_dict(cls, instance: dict):
        xrefs = {
            item.get('database'): item.get('id') for item in instance.get('obo_xref')
        } if instance.get('obo_xref') is not None else {'MESH': None}
        return cls(
            iri=instance.get('iri'),
            label=instance.get('label'),
            synonyms=[synonym for synonym in instance.get('synonyms')] if instance.get('synonyms') is not None else [],
            parent_link=instance.get('_links').get('parents').get('href'),
            mesh_xref=f"{MESH_DB_URL}/?{xrefs.get('MESH')}" if xrefs.get('MESH') is not None else None
        )


class OlsApiResourceResponse(CoreModel):
    ontologies: List[OlsApiOntologyResponse]
    current_page: int
    total_pages: int
    next_page: Optional[str]

    @classmethod
    def from_api_response(cls, instance: dict):
        return cls(
            ontologies=[
                OlsApiOntologyResponse.from_embedded_term_dict(item) for item in instance.get('_embedded').get('terms')
            ],
            current_page=instance.get('page').get('number'),
            total_pages=instance.get('page').get('totalPages'),
            next_page=instance.get('_links').get('next').get('href')
        )

    @classmethod
    def from_list(cls, instance: List[dict]):
        return cls(
            ontologies=[
                OlsApiOntologyResponse.from_embedded_term_dict(item) for item in instance
            ],
            current_page=0,
            total_pages=0,
            next_page=None
        )

    def __add__(self, other):
        return OlsApiResourceResponse(
            ontologies=self.ontologies + other.ontologies,
            current_page=None,
            total_pages=None,
            next_page=None
        )

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def get_list_of_terms_for_database_operation(self):
        return [
            TermBase(
                iri=term.iri, label=term.label, parent_link=term.parent_link, mesh_xref=term.mesh_xref
            ).dict() for term in self.ontologies
        ]

    def get_list_of_unique_synonyms_for_database_operation(self):
        return [
            TermSynonymBase(
                synonym=synonym
            ).dict() for synonym in set(chain(*[term.synonyms for term in self.ontologies]))
        ]

    def get_list_of_iri_values_for_database_operation(self):
        return [
            TermIriBase(
                iri=term.iri
            ).dict() for term in self.ontologies
        ]

    def get_list_of_unique_term_and_synonym_relationship_combinations_for_database_operation(self):
        return [
            TermSynonymRelationshipBase(
                iri=entity[0],
                synonym=entity[1]
            ).dict() for entity in set(chain(*[list(product([term.iri], term.synonyms)) for term in self.ontologies]))
        ]


class TermBase(CoreModel):
    iri: str
    label: Optional[str]
    parent_link: Optional[str]
    mesh_xref: Optional[str]

    @classmethod
    def from_ontology_response_model(cls, instance: OlsApiOntologyResponse):
        return cls(
            iri=instance.iri,
            label=instance.label,
            parent_link=instance.parent_link,
            mesh_xref=instance.mesh_xref
        )


class TermSynonymBase(CoreModel):
    synonym: str


class TermSynonymRelationshipBase(CoreModel):
    iri: str
    synonym: str


class TermIriBase(CoreModel):
    iri: str


class TermRetrieve(CoreModel):
    iri: List[str]
