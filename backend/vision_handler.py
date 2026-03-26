import base64
import os
from groq import Groq
from loguru import logger
from utils.config import settings

class VisionHandler:
    def __init__(self):
        self.api_key = settings.groq_api_key
        self.client = Groq(api_key=self.api_key) if self.api_key and self.api_key != "your_groq_api_key_here" else None

    def explain_image(self, image_path: str, user_query: str = "Explain what is in this image", language: str = "en"):
        if not self.client:
            return "Vision service not configured."
        
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
            prompt = f"{user_query}\nPlease explain in {language}."
            
            completion = self.client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{encoded_string}",
                                }
                            }
                        ]
                    }
                ],
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Vision error: {e}")
            return f"Failed to process image: {str(e)}"

vision_handler = VisionHandler()
