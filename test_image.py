import openai

import os                             # For accessing environment variables and operating system functions
from dotenv import load_dotenv        # For loading environment variables from a .env file

# Load the environment variables from .env file - the OpenAI API Key
load_dotenv()

# settings and keys
openai.api_key = os.environ.get('OPENAI_API_KEY')  # Assign OpenAI API key from environment variable


input_prompt = "A evening photo taken at Sydney harbour bridge, Australia. The weather is clear sky and 14 degrees. The date is Queen's birthday (event). Near by there are people walking, cars and train on the bridge."

response = openai.Image.create(
  prompt=input_prompt,
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']
print(image_url)