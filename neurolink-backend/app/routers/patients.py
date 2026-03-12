from fastapi import APIRouter
from app.database.supabase_client import supabase

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("/")
def create_patient(data: dict):

    response = supabase.table("patients").insert(data).execute()

    return response.data


@router.get("/")
def get_patients():

    response = supabase.table("patients").select("*").execute()

    return response.data