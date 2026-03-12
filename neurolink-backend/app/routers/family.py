from fastapi import APIRouter
from app.database.supabase_client import supabase
from app.services.face_service import identify_face

router = APIRouter(prefix="/family-members", tags=["Family Members"])


# CREATE FAMILY MEMBER
@router.post("/")
def create_family_member(data: dict):

    response = supabase.table("family_members").insert(data).execute()

    return response.data


# GET ALL FAMILY MEMBERS FOR A PATIENT
@router.get("/{patient_id}")
def get_family_members(patient_id: str):

    response = (
        supabase
        .table("family_members")
        .select("*")
        .eq("patient_id", patient_id)
        .execute()
    )

    return response.data


# REGISTER FACE EMBEDDING
@router.post("/register-face")
def register_face(data: dict):

    member_id = data["member_id"]
    embedding = data["embedding"]

    response = (
        supabase
        .table("family_members")
        .update({"face_embedding": embedding})
        .eq("id", member_id)
        .execute()
    )

    return {
        "message": "Face embedding registered successfully",
        "data": response.data
    }


# IDENTIFY FACE
@router.post("/identify")
def identify(data: dict):

    patient_id = data["patient_id"]
    embedding = data["embedding"]

    match = identify_face(patient_id, embedding)

    if match:

        return {
            "identified": True,
            "name": match["name"],
            "relationship": match["relationship"],
            "description": match["description"]
        }

    return {
        "identified": False,
        "message": "Person not recognized"
    }