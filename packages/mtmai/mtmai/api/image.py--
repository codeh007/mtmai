
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, Field
import structlog

from mtmai.llm.text2image import call_hf_text2image

router = APIRouter()
LOG = structlog.get_logger()


demo_prompt = "a woman wearing a poncho oversized puffer jacket, inspired by OffWhite, tumblr, inspired by Yanjun Cheng style, digital art, lofi girl internet meme, trending on dezeen, catalog photo, 3 d render beeple, rhads and lois van baarle, cartoon style illustration, bright pastel colors, a beautiful artwork illustration, retro anime girl <lora:iu_V35:0.5> <lora:epiNoiseoffset_v2:0.5>"


class Text2ImageRequest(BaseModel):
    prompt: str = Field(
        ..., min_length=10, description="Prompt must be at least 10 characters."
    )
    model: str | None = None


@router.post("/text2image")
async def text2image(req: Text2ImageRequest):
    """Convert text to image using a Hugging Face model."""
    try:
        image_buffer = await call_hf_text2image(prompt=req.prompt, model=req.model)
        if not image_buffer:
            raise HTTPException(status_code=500, detail="Failed to generate image")
        return Response(content=image_buffer, media_type="image/jpeg")
    except Exception as e:
        LOG.exception(f"Error generating image: {e!s}")  # noqa: G004
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/text2image1", include_in_schema=False)
async def text2image1():
    image_buffer = await call_hf_text2image(prompt="Astronaut riding a horse")
    return Response(content=image_buffer, media_type="image/jpeg")


@router.get("/text2image2", include_in_schema=False)
async def text2image2():
    image_buffer = await call_hf_text2image(
        prompt="full body photo of a beautiful Irish trans-girl, adorable face, red long layered hair, no makeup, realistic skin texture, low saturation, dark tone, inspired by Alessio Albi, f1. 4, 85mm lens, hyper realistic , lifelike texture, dramatic lighting, professional shot, heavy shadows, dynamic pose, innocent look"
    )
    return Response(content=image_buffer, media_type="image/jpeg")
