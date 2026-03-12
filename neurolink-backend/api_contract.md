# NeuroLink — Frontend Integration Guide

> **Base URL:** `http://127.0.0.1:8000`
> **CORS:** Enabled for all origins
> **Health Check:** `GET /health` → `{ "status": "running" }`

---

## 📊 Supabase Tables

| Table | Purpose |
|---|---|
| `patients` | Patient profiles |
| `family_members` | Family members with face embeddings |
| `memories` | Text memories (also stored in ChromaDB for RAG) |
| `routines` | Scheduled tasks/routines |
| `alerts` | Emergency & wandering alerts |
| `location_history` | GPS location log |
| `conversation_logs` | All assistant conversations (with intent) |
| `safe_zones` | Geofence boundaries |
| `photos` | Photo memories with embeddings |

---

## 🔗 All API Endpoints

---

### 1. Patients

#### `POST /patients/`
Register a new patient.

```json
// Request
{
  "name": "string",
  "age": 72,
  "caregiver_id": "uuid"
}

// Response → array of inserted rows
[{ "id": "uuid", "name": "...", ... }]
```

#### `GET /patients/`
List all patients.

```json
// Response
[{ "id": "uuid", "name": "...", "age": 72, ... }]
```

---

### 2. Assistant (AI Brain)

#### `POST /assistant/`
Send text to the AI assistant. Detects intent, responds, and logs the conversation.

```json
// Request
{
  "patient_id": "uuid",
  "text": "Who is my daughter?"
}

// Response
{
  "intent": "memory_query",
  "response": "Your daughter is Priya. She visited you last Sunday..."
}
```

**Possible intents:** `memory_query`, `routine_check`, `emergency`, or general fallback.

---

### 3. Voice Assistant

#### `POST /voice/command`
Process a voice command. Handles more intents than the text assistant.

```json
// Request
{
  "patient_id": "uuid",
  "text": "Where am I?"
}

// Response (varies by intent)
{
  "intent": "location_query",
  "location": [{ "latitude": 20.29, "longitude": 85.82, ... }]
}
```

**Supported intents:** `routine_check`, `memory_timeline`, `location_query`, `emergency`, `memory_query`

---

### 4. Family Members

#### `POST /family-members/`
Add a family member.

```json
// Request
{
  "patient_id": "uuid",
  "name": "Priya",
  "relationship": "daughter",
  "description": "Lives in Delhi"
}
```

#### `GET /family-members/{patient_id}`
Get all family members for a patient.

#### `POST /family-members/register-face`
Register a face embedding for recognition.

```json
// Request
{
  "member_id": "uuid",
  "embedding": [0.12, -0.34, 0.56, ...]
}

// Response
{
  "message": "Face embedding registered successfully",
  "data": [{ ... }]
}
```

#### `POST /family-members/identify`
Identify a person from a face embedding.

```json
// Request
{
  "patient_id": "uuid",
  "embedding": [0.12, -0.34, 0.56, ...]
}

// Response (matched)
{
  "identified": true,
  "name": "Priya",
  "relationship": "daughter",
  "description": "Lives in Delhi"
}

// Response (no match)
{
  "identified": false,
  "message": "Person not recognized"
}
```

---

### 5. Memories

#### `POST /memories/`
Store a new memory. Automatically creates a vector embedding in ChromaDB for RAG search.

```json
// Request
{
  "patient_id": "uuid",
  "title": "Wedding Day",
  "description": "Married in 1980 in Bhubaneswar",
  "location": "Bhubaneswar"
}

// Response
{ "id": "uuid", "title": "Wedding Day", ... }
```

#### `GET /memories/{patient_id}`
Get all memories for a patient.

---

### 6. Photos

#### `POST /photos/`
Upload a photo memory.

```json
// Request
{
  "patient_id": "uuid",
  "url": "https://storage.example.com/photo.jpg",
  "description": "Family reunion 2020"
}
```

#### `GET /photos/{patient_id}`
Get all photos for a patient.

#### `POST /photos/store-embedding`
Store a photo's vector embedding (for similarity search).

```json
// Request
{
  "photo_id": "uuid",
  "embedding": [0.12, -0.34, 0.56, ...]
}
```

---

### 7. Routines

#### `POST /routines/`
Create a routine/task.

```json
// Request
{
  "patient_id": "uuid",
  "title": "Take Medicine",
  "description": "Take blood pressure medicine",
  "time": "08:00"
}
```

#### `GET /routines/{patient_id}`
Get all routines for a patient.

---

### 8. Alerts

#### `POST /alerts/`
Create an alert manually.

```json
// Request
{
  "patient_id": "uuid",
  "alert_type": "emergency",
  "status": "active"
}
```

#### `GET /alerts/{patient_id}`
Get all alerts for a patient.

---

### 9. Location

#### `POST /location/update`
Update patient's location. Automatically checks safe zone and triggers wandering alert if outside.

```json
// Request
{
  "patient_id": "uuid",
  "latitude": 20.2961,
  "longitude": 85.8245
}

// Response
{
  "status": "location updated",
  "alert_triggered": true  // or false
}
```

#### `GET /location/{patient_id}`
Get the patient's most recent location.

```json
// Response
[{
  "patient_id": "uuid",
  "latitude": 20.2961,
  "longitude": 85.8245,
  "timestamp": "2026-03-08T11:22:09.060849"
}]
```

---

### 10. Safe Zones

#### `POST /safe-zones/`
Define a geofence safe zone.

```json
// Request
{
  "patient_id": "uuid",
  "label": "Home",
  "latitude": 20.2961,
  "longitude": 85.8245,
  "radius_meters": 200
}
```

---

### 11. Patient Summary (Caregiver Dashboard)

#### `GET /patient-summary/{patient_id}`
**Single API call** that returns everything the caregiver dashboard needs.

```json
// Response
{
  "patient": [{ "id": "uuid", "name": "...", ... }],
  "routines": [{ "title": "Take Medicine", ... }],
  "alerts": [{ "alert_type": "emergency", "status": "active", ... }],
  "last_location": [{ "latitude": 20.29, "longitude": 85.82, ... }],
  "recent_conversations": [{
    "user_message": "Who is my daughter?",
    "assistant_response": "Your daughter is Priya...",
    "intent": "memory_query",
    ...
  }]
}
```

> **Note:** Alerts are filtered to `status = "active"` only. Location ordered by `timestamp`. Conversations limited to latest 5.

---

### 12. Debug (Dev Only)

#### `GET /debug/vectors`
View all stored ChromaDB vector embeddings.

---

## 🏗️ Suggested Frontend Pages

### Patient Interface (Mobile)
| Feature | API Used |
|---|---|
| Voice assistant button | `POST /voice/command` |
| Text chat | `POST /assistant/` |
| Camera face recognition | `POST /family-members/identify` |
| Emergency help button | `POST /alerts/` |
| Memory timeline | `GET /memories/{patient_id}` |
| Photo gallery | `GET /photos/{patient_id}` |

### Caregiver Dashboard (Web)
| Feature | API Used |
|---|---|
| Patient overview | `GET /patient-summary/{patient_id}` |
| Routine manager | `GET/POST /routines/` |
| Alerts monitor | `GET /alerts/{patient_id}` |
| Live location map | `GET /location/{patient_id}` |
| Memory uploads | `POST /memories/` |
| Photo uploads | `POST /photos/` |
| Family member management | `GET/POST /family-members/` |
| Set safe zones | `POST /safe-zones/` |
| Conversation history | via `/patient-summary` |

---

## ⚡ Quick Start for Frontend

```javascript
// Example: Fetch patient summary
const BASE_URL = "http://127.0.0.1:8000";

const res = await fetch(`${BASE_URL}/patient-summary/${patientId}`);
const data = await res.json();

// Example: Send message to assistant
const res = await fetch(`${BASE_URL}/assistant/`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    patient_id: patientId,
    text: "What should I do now?"
  })
});
const { intent, response } = await res.json();
```

---

## 📝 Notes for Frontend Dev

1. **All IDs are UUIDs** generated by Supabase
2. **CORS is enabled** — frontend can call from any origin
3. **No authentication** is implemented yet — add later if needed
4. **Face embeddings** should be generated client-side (using TensorFlow.js / face-api.js) and sent as arrays of floats
5. **Location updates** should be sent periodically from the patient's device (use browser Geolocation API or mobile GPS)
6. **Interactive docs** available at `http://127.0.0.1:8000/docs` (Swagger UI)
