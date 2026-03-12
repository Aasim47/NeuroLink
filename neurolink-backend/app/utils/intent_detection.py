def detect_intent(text: str):

    text = text.lower()

    # Face recognition
    if "who is this" in text:
        return "face_recognition"

    # Routine
    if "what should i do" in text or "my routine" in text:
        return "routine_check"

    # Location
    if "where am i" in text:
        return "location_query"

    # Emergency
    if "help me" in text or "emergency" in text:
        return "emergency"

    # Memory queries
    memory_keywords = [
        "memory",
        "remember",
        "trip",
        "family",
        "tell me about",
        "who is",
        "when did",
        "what happened"
    ]

    for word in memory_keywords:
        if word in text:
            return "memory_query"

    return "general_chat"