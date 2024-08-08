import numpy as np
from gtts import gTTS
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from tempfile import NamedTemporaryFile
import os

def create_video(images, texts, output_path):
    clips = []
    for img, text in zip(images, texts):
        img_array = np.array(img)
        tts = gTTS(text=text, lang='en')
        with NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            tts.save(temp_audio_file.name)
            audio_clip = AudioFileClip(temp_audio_file.name)
            img_clip = ImageClip(img_array).set_duration(audio_clip.duration).set_audio(audio_clip)
            clips.append(img_clip)
            temp_audio_file.close()  # Close the temp file to ensure it's written
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_path, fps=24, audio_codec='aac')
