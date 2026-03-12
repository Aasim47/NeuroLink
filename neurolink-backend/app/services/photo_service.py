from app.database.supabase_client import supabase
from app.services.ai_service import generate_memory_response


def explain_photo(memory_id):

    memory = (
        supabase
        .table("memories")
        .select("*")
        .eq("id", memory_id)
        .execute()
    )

    if not memory.data:
        return "I could not find information about this photo."

    memory_data = memory.data[0]

    context = f"""
    Memory Title: {memory_data['title']}
    Description: {memory_data['description']}
    Location: {memory_data['location']}
    Year: {memory_data['year']}
    """

    response = generate_memory_response(context, "Explain this photo")

    return response 