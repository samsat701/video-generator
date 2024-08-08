from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from app.models.prompt_request import PromptRequest
from app.utils.generate_script import generate_script
from app.utils.download_image import download_image
from app.utils.crop_image import crop_to_9_16
from app.utils.add_caption import add_caption_to_image
from app.utils.create_video import create_video

app = FastAPI()

@app.post("/generate_video")
def generate_video(prompt_request: PromptRequest):
    prompt = prompt_request.prompt

    # Generate script
    script = generate_script(prompt)
    script_parts = script.split('. ')
    if len(script_parts) > 5:
        script_parts = script_parts[:5]
    
    # Generate images and add captions
    images = []
    for part in script_parts:
        image = download_image(part)
        if image:
            cropped_image = crop_to_9_16(image)
            captioned_image = add_caption_to_image(cropped_image, part)
            images.append(captioned_image)
    
    # Create video
    output_path = "/tmp/motivationalstory.mp4"
    create_video(images, script_parts, output_path)
    
    return FileResponse(output_path, media_type='video/mp4', filename='motivationalstory.mp4')
