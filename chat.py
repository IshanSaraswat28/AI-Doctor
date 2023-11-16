import openai
import pyttsx3
import speech_recognition as sr
from time import time, sleep
from halo import Halo


# Initialize the text-to-speech engine
engine = pyttsx3.init()

voices = engine.getProperty('voices')

# Set the voice to a female voice (you may need to adjust the index based on the available voices on your system)
engine.setProperty('voice', voices[1].id)

# Set the OpenAI API key
openai.api_key = "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"

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Function to add text to the conversation
def add_to_conversation(text, role="AI Bot"):
    print(f"{role}: {text}")
    speak_text(text)

# Function to speak the text
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Function to convert speech to text
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            user_input = recognizer.recognize_google(audio)
            print(f"You (Voice): {user_input}")
            return user_input
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"Speech Recognition error: {str(e)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

# Function to interact with the chatbot
def chatbot(conversation, model="gpt-3.5-turbo", temperature=0, max_tokens=3000):
    max_retry = 7
    retry = 0
    while True:
        try:
            spinner = Halo(text='Thinking...', spinner='dots')
            spinner.start()
            
            response = openai.ChatCompletion.create(model=model, messages=conversation, temperature=temperature, max_tokens=max_tokens)
            text = response['choices'][0]['message']['content']

            spinner.stop()
            
            return text, response['usage']['total_tokens']
        except Exception as oops:
            print(f'\n\nError communicating with OpenAI: "{oops}"')
            exit(5)

# Function to interact with the chatbot
def chat_with_bot(conversation):
    while True:
        text = recognize_speech()
        if not text:
            continue

        user_messages.append(text)
        all_messages.append(f'PATIENT: {text}')
        conversation.append({'role': 'user', 'content': text})

        response, tokens = chatbot(conversation)
        conversation.append({'role': 'assistant', 'content': response})
        all_messages.append(f'INTAKE: {response}')
        add_to_conversation(response)

        if text.lower() == 'done':
            break

if __name__ == '__main__':
    user_messages = list()
    all_messages = list()
    conversation = [{'role': 'system', 'content': 'Initializing chatbot...'}]

    print('Describe your symptoms to the intake bot. Say "DONE" when done.')

    chat_with_bot(conversation)
