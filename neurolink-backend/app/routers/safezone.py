from fastapi import APIRouter
from app.database.supabase_client import supabase

router = APIRouter(prefix="/safe-zones", tags=["Safe Zones"])


@router.post("/")
def create_safe_zone(data: dict):

    response = supabase.table("safe_zones").insert(data).execute()

    return response.data