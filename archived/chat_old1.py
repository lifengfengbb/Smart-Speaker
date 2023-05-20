# Import necessary libraries
import openai                         # For accessing OpenAI API
import os                             # For accessing environment variables and operating system functions
import pyaudio                        # For audio I/O
import speech_recognition as sr       # For converting speech to text
from gtts import gTTS                 # For converting text to speech from Google
from playsound import playsound       # For playing sound files
from dotenv import load_dotenv        # For loading environment variables from a .env file

# Load the environment variables from .env file - the OpenAI API Key
load_dotenv()

# settings and keys
openai.api_key = os.environ.get('OPENAI_API_KEY')  # Assign OpenAI API key from environment variable
model_engine = "gpt-3.5-turbo"                  # text-davinci-003 Define the model engine to be used
language = 'en'                                    # Define the language to be used by Google Text-to-Speech


# Define the system message
system_msg = 'You are a helpful assistant who understands data science.'

# Define the user message
user_msg = 'tell me a joke about SQL developer.'

# Create a dataset using GPT
response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                        messages=[{"role": "system", "content": system_msg},
                                         {"role": "user", "content": user_msg}])

print(response["choices"][0]["message"]["content"])
