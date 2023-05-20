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
language_out = 'en'     #en                               # Define the language to be used by Google Text-to-Speech
language_in = 'en-AU'

# This function recognizes the wake word from the speech
def recognize_speech():
    # obtain audio from the microphone
    r = sr.Recognizer()
    # Use the default system microphone
    with sr.Microphone() as source:
        print("Waiting for wake word...")
        while True:
            try:
                # Calibrate the recognizer to the noise level of the audio source
                r.adjust_for_ambient_noise(source)
                # Listen to the source
                audio_stream = r.listen(source)
                # recognize speech using Google Speech Recognition
                try:
                    # Print what Google Speech Recognition thinks you said
                    print("Google Speech Recognition thinks you said:\n" + r.recognize_google(audio_stream, language=language_in))
                    # Recognize the speech
                    speech = r.recognize_google(audio_stream, language=language_in)
                    # If the wake word is not detected in the speech
                    if ("GPT" not in speech) and ("gpt" not in speech):
                        # the wake word was not detected in the speech
                        print("Wake word not detected in the speech")
   						# Close the current microphone object
                        return False
                    else:
                        # the wake word was detected in the speech
                        print("Found wake word!")
                        # wake up the display
                        #pixels.wakeup()
                        return True
                except sr.UnknownValueError:
                    # If Google Speech Recognition could not understand the audio
                    print("Google Speech Recognition could not understand audio")
                    print("Waiting for wake word...")
                    return False
                except sr.RequestError as e:
                    # If there is a request error from Google Speech Recognition
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
                    print("Waiting for wake word...")
                    return False
            except KeyboardInterrupt:
                # If the user interrupts the program
                print("Interrupted by User Keyboard")
                break

# This function listens to the user's speech
def speech():
    # obtain audio from the microphone
    r = sr.Recognizer()
    # Use the default system microphone
    with sr.Microphone() as source:
        print("Waiting for user to speak...")
        while True:
            try:
                # Calibrate the recognizer to the noise level of the audio source
                r.adjust_for_ambient_noise(source)
                 # Listen to the source
                audio_stream = r.listen(source)
                # recognize speech using Google Speech Recognition
                try:
                    # Print what Google Speech Recognition thinks you said
                    print("Google Speech Recognition thinks you said:\n" + r.recognize_google(audio_stream, language=language_in))
                    # Recognize the speech
                    speech = r.recognize_google(audio_stream, language=language_in)
                    # wake up thinking LEDs
                    #pixels.think()
                    return speech
                except sr.UnknownValueError:
                    # If Google Speech Recognition could not understand the audio
                    print("Google Speech Recognition could not understand audio")
                    #pixels.off()
                    print("Waiting for user to speak...")
                    continue
                except sr.RequestError as e:
                    # If there is a request error from Google Speech Recognition
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
                    #pixels.off()
                    print("Waiting for user to speak...")
                    continue
            except KeyboardInterrupt:
                # If the user interrupts the program
                print("Interrupted by User Keyboard")
                break

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

# Define a function to generate an audio file from GPT text response
def generate_audio_file(text):
    # convert the text response from chatgpt to an audio file 
    audio = gTTS(text=text, lang=language_out, slow=False)
    # save the audio file
    audio.save("response.mp3")

# Define a function to play the audio file
def play_audio_file():
    # play the audio file and wake speaking LEDs
    #pixels.speak()
    # os.system("mpg321 response.mp3")
    # Play the audio file asynchronously
    playsound("response.mp3") 


# Main function to orchestrate all the actions
def main():
    # Run the program continuously
    while True:
        # If wake word is detected in the speech
        if recognize_speech():
            # Capture further user speech as a prompt for chatbot
            prompt = speech()
            print(f"This is the prompt being sent to OpenAI:\n" + prompt)
            message = llm_chain.predict(question=prompt)
            print(f"This is the message from OpenAI:\n" + message)
            generate_audio_file(message)
            play_audio_file()
        else:
            # If wake word is not detected, print error message and turn off LEDs
            print("Wake word was not recognised")
            #pixels.off()

if __name__ == "__main__":
    main()