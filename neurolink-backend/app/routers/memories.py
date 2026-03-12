from fastapi import APIRouter
from app.database.supabase_client import supabase
from app.services.rag_service import store_memory_embedding

router = APIRouter(prefix="/memories", tags=["Memories"])


@router.post("/")
def create_memory(data: dict):

    response = supabase.table("memories").insert(data).execute()

    memory = response.data[0]

    text = f"{memory['title']} {memory['description']} {memory['location']}"

    store_memory_embedding(memory["id"], text)

    return memory


@router.get("/{patient_id}")
def get_memories(patient_id: str):

    response = (
        supabase.table("memories")
        .select("*")
        .eq("patient_id", patient_id)
        .execute()
    )

    return response.data