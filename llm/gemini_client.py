import os
from google import genai
from google.genai import types
import dotenv

dotenv.load_dotenv()
async def generate_explanation(prompt: str) -> str:
    """
    Sends a prompt to Gemini 2.0 Flash and returns the text response.
    """
    # 1. Fetch the key inside the function (Lazy Loading)
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
        
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing. Please check your .env file.")

    client = genai.Client(api_key=api_key)

    response = await client.aio.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=1000 
        )
    )

    return response.text.strip()