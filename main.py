import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import httpx

load_dotenv()

TRPC_BASE_URL = os.getenv("TRPC_BASE_URL", "").rstrip("/")
app = FastAPI()

class TeacherRequest(BaseModel):
    lesson_id: int
    student_message: str
    action: str = "next"
    student_language: str = "en"
    lesson_phase: str = "explanation"

@app.get("/api/python/health")
def health():
    return {"ok": True}

@app.post("/api/python/teacher/response")
async def teacher_response(req: TeacherRequest, request: Request):
    manus_session = request.cookies.get("manus_session")
    if not manus_session:
        raise HTTPException(status_code=401, detail="Missing manus_session cookie")

    url = f"{TRPC_BASE_URL}/api/trpc/auth.me"
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url, headers={"Cookie": f"manus_session={manus_session}"})
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid session")

    return {
        "message": "Python backend is connected ✅",
        "phase": req.lesson_phase,
        "is_question": False
    }
