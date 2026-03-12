from fastapi import APIRouter
from app.database.supabase_client import supabase
from app.services.location_service import check_safe_zone

router = APIRouter(prefix="/location", tags=["Location"])



@router.post("/update")
def update_location(data: dict):

    patient_id = data["patient_id"]
    lat = data["latitude"]
    lng = data["longitude"]

    supabase.table("location_history").insert(data).execute()

    alert = check_safe_zone(patient_id, lat, lng)

    return {
        "status": "location updated",
        "alert_triggered": alert
    }

@router.get("/{patient_id}")
def get_location(patient_id: str):

    response = (
        supabase.table("location_history")
        .select("*")
        .eq("patient_id", patient_id)
        .order("timestamp", desc=True)
        .limit(1)
        .execute()
    )

    return response.data