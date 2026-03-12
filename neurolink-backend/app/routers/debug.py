from fastapi import APIRouter
from app.vector.chroma_client import collection

router = APIRouter(prefix="/debug", tags=["Debug"])


@router.get("/vectors")
def check_vectors():

    data = collection.get()

    return data