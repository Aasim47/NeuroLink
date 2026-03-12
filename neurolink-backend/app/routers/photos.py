from fastapi import APIRouter
from app.database.supabase_client import supabase

router = APIRouter(prefix="/photos", tags=["Photos"])


@router.post("/")
def upload_photo(data: dict):

    response = supabase.table("photos").insert(data).execute()

    return response.data


@router.get("/{patient_id}")
def get_photos(patient_id: str):

    response = (
        supabase
        .table("photos")
        .select("*")
        .eq("patient_id", patient_id)
        .execute()
    )

    return response.data


@router.post("/store-embedding")
def store_embedding(data: dict):

    photo_id = data["photo_id"]
    embedding = data["embedding"]

    # convert to pgvector format
    vector_string = "[" + ",".join(map(str, embedding)) + "]"

    response = (
        supabase
        .table("photos")
        .update({"embedding_vector": vector_string})
        .eq("id", photo_id)
        .execute()
    )

    return response.data