from fastapi import APIRouter

router = APIRouter()


@router.get("/tts", include_in_schema=False)
async def tts():
    return "hello_tts"
