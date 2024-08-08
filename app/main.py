import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.utils.generate_script import generate_script
from app.utils.download_image import download_image
from app.utils.crop_image import crop_to_9_16
from app.utils.add_caption import add_caption_to_image
from app.utils.create_video import create_video

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate_video")
def generate_video(prompt_request: PromptRequest):
    prompt = prompt_request.prompt
    logger.info(f"Received prompt: {prompt}")

    # Generate script
    script = generate_script(prompt)
    logger.info(f"Generated script: {script}")
    script_parts = script.split('. ')
    if len(script_parts) > 5:
        script_parts = script_parts[:5]
    logger.info(f"Script parts: {script_parts}")
    
    # Generate images and add captions
    images = []
    for part in script_parts:
        image = download_image(part)
        if image:
            cropped_image = crop_to_9_16(image)
            captioned_image = add_caption_to_image(cropped_image, part)
            images.append(captioned_image)
            logger.info(f"Generated image for part: {part}")
        else:
            logger.error(f"Failed to download image for part: {part}")
    
    # Create video
    output_path = "/tmp/motivationalstory.mp4"
    create_video(images, script_parts, output_path)
    logger.info(f"Video created at: {output_path}")
    
    return FileResponse(output_path, media_type='video/mp4', filename='motivationalstory.mp4')
