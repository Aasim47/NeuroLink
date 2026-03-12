from fastapi import APIRouter
from app.utils.intent_detection import detect_intent
from app.database.supabase_client import supabase
from app.services.rag_service import search_memories
from app.services.ai_service import generate_memory_response

router = APIRouter(prefix="/voice", tags=["Voice Assistant"])


@router.post("/command")
def voice_command(data: dict):

    patient_id = data["patient_id"]
    text = data["text"]

    intent = detect_intent(text)

    # ROUTINE CHECK
    if intent == "routine_check":

        routines = (
            supabase.table("routines")
            .select("*")
            .eq("patient_id", patient_id)
            .execute()
        )

        if routines.data:
            routine = routines.data[0]

            return {
                "intent": intent,
                "response": f"It is time to {routine['title']}"
            }

        return {
            "intent": intent,
            "response": "You have no scheduled routines."
        }

    # MEMORY REQUEST
    if intent == "memory_timeline":

        memories = (
            supabase.table("memories")
            .select("*")
            .eq("patient_id", patient_id)
            .execute()
        )

        return {
            "intent": intent,
            "memories": memories.data
        }

    # LOCATION
    if intent == "location_query":

        location = (
            supabase.table("location_history")
            .select("*")
            .eq("patient_id", patient_id)
            .order("timestamp", desc=True)
            .limit(1)
            .execute()
        )

        return {
            "intent": intent,
            "location": location.data
        }

    # EMERGENCY
    if intent == "emergency":

        supabase.table("alerts").insert({
            "patient_id": patient_id,
            "alert_type": "emergency"
        }).execute()

        response_text = "Emergency alert sent to caregiver."

        supabase.table("conversation_logs").insert({
            "patient_id": patient_id,
            "user_message": text,
            "assistant_response": response_text,
            "intent": intent
        }).execute()

        return {
            "intent": intent,
            "response": response_text
        }
    
    if intent == "memory_query":

        context = search_memories(text)

        if context:

            response = generate_memory_response(context, text)

            return {
                "intent": intent,
                "response": response
            }

    return {
        "intent": intent,
        "response": "I could not find a related memory."
    }