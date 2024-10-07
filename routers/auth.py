from fastapi import APIRouter

router = APIRouter()

@router.get("/auth/")
async def authentication():
    return {"message": "successfully Loaded"}