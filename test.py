import openai
import whisper
import pyttsx3
from transformers import GPT2TokenizerFast
import speech_recognition as sr

import gtts
from playsound import playsound

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


class Patient:

    def __init__(self, instructions):
        self.engine = pyttsx3.init()
        self.memory = [{"role": "system", "content": instructions}]
        self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        self.tokens = len(self.tokenizer(instructions)['input_ids'])
        self.max_tokens = 4000
        self.r = sr.Recognizer()
        self.model = whisper.load_model("base")

    def transcribe(self, audio):
        try:
            with open("audio.wav", "wb") as f:
                f.write(audio.get_wav_data())
            return self.model.transcribe('audio.wav', language='en', fp16=False)['text']
        except:
            return None

    def generate_response(self, prompt):
        self.update_memory("user", prompt)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # model='gpt-4',
            messages=self.memory,
            temperature=0,
            top_p=1,)['choices'][0]['message']['content']
        self.update_memory("system", response)
        return response

    def speak(self, text):
        gtts.gTTS(text).save("output.mp3")
        playsound("output.mp3")

    def update_memory(self, role, content):
        self.memory.append({"role": role, "content": content})
        self.tokens += len(self.tokenizer(content)['input_ids'])
        while self.tokens > self.max_tokens:
            popped = self.memory.pop(0)
            self.tokens -= len(self.tokenizer(popped['content'])['input_ids'])

    def main(self):
        print("Clinical scenario starting...")
        while True:
            print("Me: ", end='')
            with sr.Microphone() as source:
                source.pause_threshold = 0.8  # silence in seconds
                audio = self.r.listen(source)
            text = self.transcribe(audio)
            if text:
                print(text)
                response = self.generate_response(text)
                print(f"Patient: {response}\n")
                self.speak(response)

if __name__ == "__main__":
    instructions = "You are a patient in a family medicine practice. Your name is Joanna. You are 35 years old female. You have a sore throat. You have a history of asthma and allergies. You are in for a general checkup to review your medications. You are currently on Advair and have well-controlled asthma. Please answer questions based on a presentation of well controlled asthma. Please answer questions like a patient. Do not give too much away unless asked. You may use creativity in your answers."
    patient = Patient(instructions)
    patient.main()
