from fastapi import APIRouter
from api.routes.ontology import router as ontology_router

router = APIRouter()

router.include_router(ontology_router, prefix='/ontology', tags=['ontology'])
