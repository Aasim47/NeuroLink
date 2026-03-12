from fastapi import APIRouter
from app.database.supabase_client import supabase

router = APIRouter(prefix="/patient-summary", tags=["Patient Summary"])


@router.get("/{patient_id}")
def get_patient_summary(patient_id: str):

    # patient info
    patient = (
        supabase
        .table("patients")
        .select("*")
        .eq("id", patient_id)
        .execute()
    )

    # routines
    routines = (
        supabase
        .table("routines")
        .select("*")
        .eq("patient_id", patient_id)
        .execute()
    )

    # recent active alerts
    alerts = (
        supabase
        .table("alerts")
        .select("*")
        .eq("patient_id", patient_id)
        .eq("status", "active")
        .order("created_at", desc=True)
        .limit(5)
        .execute()
    )

    # last location
    location = (
        supabase
        .table("location_history")
        .select("*")
        .eq("patient_id", patient_id)
        .order("timestamp", desc=True)
        .limit(1)
        .execute()
    )

    # recent conversations
    conversations = (
        supabase
        .table("conversation_logs")
        .select("*")
        .eq("patient_id", patient_id)
        .order("created_at", desc=True)
        .limit(5)
        .execute()
    )

    return {
        "patient": patient.data,
        "routines": routines.data,
        "alerts": alerts.data,
        "last_location": location.data,
        "recent_conversations": conversations.data
    }