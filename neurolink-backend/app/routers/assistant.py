from fastapi import APIRouter
from app.utils.intent_detection import detect_intent
from app.services.rag_service import search_memories
from app.services.conversation_service import get_recent_conversations, store_conversation
from app.services.ai_service import generate_ai_response
from app.database.supabase_client import supabase

router = APIRouter(prefix="/assistant", tags=["Assistant"])


@router.post("/")
def assistant(data: dict):

    patient_id = data["patient_id"]
    text = data["text"]

    # fetch recent conversation history
    history = get_recent_conversations(patient_id)

    context = ""

    for convo in history:
        context += f"User: {convo['user_message']}\n"
        context += f"Assistant: {convo['assistant_response']}\n"

    intent = detect_intent(text)

    if intent == "memory_query":

        memory = search_memories(text)

        if memory:

            prompt = f"""
            You are an AI assistant helping an Alzheimer’s patient remember past events.

            Explain the memory clearly and calmly.

            Rules:
            - Use simple sentences
            - Be brief
            - Do not invent details
            - Focus on who, where, and what

            Memory:
            {memory}
            """

            ai_response = generate_ai_response(prompt)

            response = ai_response

        else:
            response = "I couldn't find a related memory."


    elif intent == "routine_check":

        routines = (
            supabase
            .table("routines")
            .select("*")
            .eq("patient_id", patient_id)
            .execute()
        )

        if routines.data:
            routine = routines.data[0]
            response = f"You should {routine['description']}."
        else:
            response = "You have no scheduled tasks right now."


    elif intent == "emergency":

        supabase.table("alerts").insert({
            "patient_id": patient_id,
            "alert_type": "emergency",
            "status": "active"
        }).execute()

        response = "Emergency alert sent to caregiver."


    else:

        response = "I'm here to help you."

    # store conversation
    store_conversation(patient_id, text, response, intent)

    return {
        "intent": intent,
        "response": response
    }