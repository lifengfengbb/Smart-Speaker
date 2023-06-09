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
model_engine = "gpt-3.5-turbo"                  # text-davinci-003 Define the model engine to be used
language_out = 'zh'     #en                               # Define the language to be used by Google Text-to-Speech
language_in = 'zh'

# Define a function to recognize speech using Google Speech Recognition
def recognize_speech():
    # obtain audio from the microphone
    r = sr.Recognizer()  # Create an instance of the recognizer class
    with sr.Microphone() as source:  # Use the default system microphone as the audio source
        print("Say something!")
        audio = r.listen(source)  # Listen to the source

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        # convert the audio to text
        
        # transcript = openai.Audio.transcribe("whisper-1", audio)
        # speech = transcript["text"]
        # print("Whisper thinks you said:\n" + speech)

        print("Google Speech Recognition thinks you said:\n" + r.recognize_google(audio, language=language_in))  # Convert audio to text and print it
        speech = r.recognize_google(audio, language=language_in)  # Store the recognized speech
        print("This is what we think was said:\n" + speech)  # Print the recognized speech
    except sr.UnknownValueError:  # Handle case where speech was unintelligible
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:  # Handle case where a request error occurred
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return speech  # Return the recognized speech


template = """You are a helpful assistant who understands me.
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

# Define a function to get a response from GPT
# def chatgpt_response(prompt):
#     # send the converted audio text to chatgpt
#     response = openai.ChatCompletion.create(
#         model=model_engine,
#         messages=[{"role": "system", "content": system_msg},
#                   {"role": "user", "content": prompt}]
#     )
#     return response


# Define a function to generate an audio file from GPT text response
def generate_audio_file(text):
    # convert the text response from chatgpt to an audio file 
    audio = gTTS(text=text, lang=language_out, slow=False)
    # save the audio file
    audio.save("response.mp3")

# Define a function to play the audio file
def play_audio_file():
    # play the audio file
    #os.system("start response.mp3")       # Use the mpg321 command-line mp3 player to play the audio
    #playsound("response.mp3", block=False) # There’s an optional second argument, block, which is set to True by default. Setting it to False makes the function run asynchronously.
    playsound("response.mp3") 


# Define a function to run the program
def main():
    # run the program
    while True:
        prompt = recognize_speech()  # Recognize speech and use it as the prompt for GPT
        print(f"This is the prompt being sent to OpenAI:\n" + prompt)  # Print the prompt
        # responses = chatgpt_response(prompt)  # Get a response from GPT
        # message = responses["choices"][0]["message"]["content"]  # Extract the text from the response
        message = llm_chain.predict(question=prompt)
        print(f"This is the message from OpenAI:\n" + message)
        generate_audio_file(message)
        play_audio_file()

if __name__ == "__main__":
    main()