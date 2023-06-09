import openai

import os                             # For accessing environment variables and operating system functions
from dotenv import load_dotenv        # For loading environment variables from a .env file

# Load the environment variables from .env file - the OpenAI API Key
load_dotenv()

# settings and keys
openai.api_key = os.environ.get('OPENAI_API_KEY')  # Assign OpenAI API key from environment variable
model_engine = "gpt-3.5-turbo"                  # text-davinci-003 Define the model engine to be used
language_out = 'zh'     #en                               # Define the language to be used by Google Text-to-Speech
language_in = 'zh'

audio_file= open("C:/Users/lifen/github/Smart-Speaker/recording_zh.mp3", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
print(transcript["text"])