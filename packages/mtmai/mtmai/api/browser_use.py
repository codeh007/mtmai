from fastapi import APIRouter

router = APIRouter()


@router.get("/health2", include_in_schema=False)
async def health_check():
    return {"status": "ok"}
