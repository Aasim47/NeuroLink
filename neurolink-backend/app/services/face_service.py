import numpy as np
from app.database.supabase_client import supabase


def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def identify_face(patient_id, embedding):

    members = (
        supabase
        .table("family_members")
        .select("*")
        .eq("patient_id", patient_id)
        .execute()
    )

    best_match = None
    best_score = 0

    for member in members.data:

        stored_embedding = member.get("face_embedding")

        if not stored_embedding:
            continue

        score = cosine_similarity(embedding, stored_embedding)

        print("Comparing with:", member["name"], "Score:", score)

        if score > best_score:
            best_score = score
            best_match = member

    # stricter threshold
    THRESHOLD = 0.85

    if best_match and best_score > THRESHOLD:
        return best_match

    return None