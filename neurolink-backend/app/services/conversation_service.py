from app.database.supabase_client import supabase


def get_recent_conversations(patient_id, limit=5):

    response = (
        supabase
        .table("conversation_logs")
        .select("*")
        .eq("patient_id", patient_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data


def store_conversation(patient_id, user_message, assistant_response, intent):

    supabase.table("conversation_logs").insert({
        "patient_id": patient_id,
        "user_message": user_message,
        "assistant_response": assistant_response,
        "intent": intent
    }).execute()