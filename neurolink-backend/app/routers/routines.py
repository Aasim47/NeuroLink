from fastapi import APIRouter
from app.database.supabase_client import supabase

router = APIRouter(prefix="/routines", tags=["Routines"])


@router.post("/")
def create_routine(data: dict):

    response = supabase.table("routines").insert(data).execute()

    return response.data


@router.get("/{patient_id}")
def get_routines(patient_id: str):

    response = supabase.table("routines").select("*").eq("patient_id", patient_id).execute()

    return response.data