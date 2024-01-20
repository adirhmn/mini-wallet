from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def check_app():
    # Check whether the application is running
    return {"status": "success", "message": "App running well"}