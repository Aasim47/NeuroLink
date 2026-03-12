import math
from app.database.supabase_client import supabase


def distance(lat1, lon1, lat2, lon2):

    R = 6371000

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2

    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))


def check_safe_zone(patient_id, lat, lng):

    zone = (
        supabase
        .table("safe_zones")
        .select("*")
        .eq("patient_id", patient_id)
        .execute()
    )

    if not zone.data:
        return False

    zone = zone.data[0]

    dist = distance(
        lat,
        lng,
        zone["center_lat"],
        zone["center_lng"]
    )

    if dist > zone["radius_meters"]:

        supabase.table("alerts").insert({
            "patient_id": patient_id,
            "alert_type": "wandering",
            "status": "active",
            "latitude": lat,
            "longitude": lng
        }).execute()

        return True

    return False