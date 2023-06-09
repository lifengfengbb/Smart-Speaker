# Import necessary libraries
import openai                         # For accessing OpenAI API
import os                             # For accessing environment variables and operating system functions
import pyaudio                        # For audio I/O
import speech_recognition as sr       # For converting speech to text
from gtts import gTTS                 # For converting text to speech from Google
from playsound import playsound       # For playing sound files
from dotenv import load_dotenv        # For loading environment variables from a .env file

from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain, PromptTemplate

# Load the environment variables from .env file - the OpenAI API Key
load_dotenv()

# settings and keys
openai.api_key = os.environ.get('OPENAI_API_KEY')  # Assign OpenAI API key from environment variable
model_engine = "gpt-3.5-turbo"                  # "gpt-4" "text-davinci-003" Define the model engine to be used
language = 'en'                                    # Define the language to be used by Google Text-to-Speech


template = """You are a teacher in physics for High School student. Given the text of question, it is your job to write a answer that question with example.
{chat_history}
Human: {question}
AI:
"""
prompt_template = PromptTemplate(input_variables=["chat_history","question"], template=template)
memory = ConversationBufferMemory(memory_key="chat_history")

llm_chain = LLMChain(
    llm=OpenAI(),
    prompt=prompt_template,
    verbose=True,
    memory=memory,
)

while True:
    value = input("Please enter a prompt:\n")
    print(f'You entered {value}')
    result = llm_chain.predict(question=value)
    print(f"Message from OpenAI:\n" + result)

