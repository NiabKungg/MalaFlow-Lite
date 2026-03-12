import os
from fastapi import APIRouter
from schemas import PinVerify
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api", tags=["auth"])

ADMIN_PIN = os.getenv("ADMIN_PIN", "1234")


@router.post("/verify")
def verify_pin(payload: PinVerify):
    if payload.pin == ADMIN_PIN:
        return {"success": True}
    return {"success": False}
