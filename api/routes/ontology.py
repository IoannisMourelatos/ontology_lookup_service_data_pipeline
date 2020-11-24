from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_202_ACCEPTED

from models.ontology import TermRetrieve
from db.repositories.ontology import OntologyRepository
from api.dependencies.database import get_repository


router = APIRouter()


@router.post("/term_from_iri", name="ontology:retrieve_term_information", status_code=HTTP_202_ACCEPTED)
async def retrieve_term(
    terms_to_retrieve: TermRetrieve = Body(..., embed=True),
    ontology_repo: OntologyRepository = Depends(get_repository(OntologyRepository)),
) -> dict:
    result = await ontology_repo.retrieve_terms(terms_to_retrieve=terms_to_retrieve)
    return {'message': 'Retrieval task completed successfully'}


@router.post("/all_terms", name="ontology:retrieve_all_terms_information", status_code=HTTP_202_ACCEPTED)
async def retrieve_terms(
    ontology_repo: OntologyRepository = Depends(get_repository(OntologyRepository)),
) -> dict:
    result = await ontology_repo.retrieve_all_terms()
    return {'message': 'Retrieval task completed successfully'}
