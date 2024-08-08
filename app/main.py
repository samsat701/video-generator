import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.utils.generate_script import generate_script
from app.utils.download_image import download_image
from app.utils.crop_image import crop_to_9_16
from app.utils.add_caption import add_caption_to_image
from app.utils.create_video import create_video
import os

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
    try:
        script = generate_script(prompt)
        logger.info(f"Generated script: {script}")
        script_parts = script.split('. ')
        if len(script_parts) > 5:
            script_parts = script_parts[:5]
        logger.info(f"Script parts: {script_parts}")
    except Exception as e:
        logger.error(f"Error generating script: {e}")
        raise HTTPException(status_code=500, detail="Error generating script")

    # Generate images and add captions
    images = []
    for part in script_parts:
        try:
            image = download_image(part)
            if image:
                cropped_image = crop_to_9_16(image)
                captioned_image = add_caption_to_image(cropped_image, part)
                images.append(captioned_image)
                logger.info(f"Generated image for part: {part}")
            else:
                logger.error(f"Failed to download image for part: {part}")
                raise HTTPException(status_code=500, detail="Failed to download image")
        except Exception as e:
            logger.error(f"Error processing part: {part}, Error: {e}")
            raise HTTPException(status_code=500, detail=f"Error processing part: {part}")

    # Create video
    output_path = "/tmp/motivationalstory.mp4"
    try:
        create_video(images, script_parts, output_path)
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            logger.info(f"Video created at: {output_path}, size: {file_size} bytes")
            if file_size == 0:
                raise HTTPException(status_code=500, detail="Generated video file is empty")
        else:
            logger.error(f"Video file was not created")
            raise HTTPException(status_code=500, detail="Video file was not created")
    except Exception as e:
        logger.error(f"Error creating video: {e}")
        raise HTTPException(status_code=500, detail="Error creating video")
    
    return FileResponse(output_path, media_type='video/mp4', filename='motivationalstory.mp4')
