from fastapi import APIRouter
from app.database.supabase_client import supabase

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.post("/")
def create_alert(data: dict):

    response = supabase.table("alerts").insert(data).execute()

    return response.data


@router.get("/{patient_id}")
def get_alerts(patient_id: str):

    response = supabase.table("alerts").select("*").eq("patient_id", patient_id).execute()

    return response.data