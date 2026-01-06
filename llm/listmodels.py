import os
from google import genai
import dotenv

dotenv.load_dotenv()

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

models = client.models.list()
for model in models:
    print(model.name)