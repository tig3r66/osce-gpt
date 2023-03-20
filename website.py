import streamlit as st
import openai
import whisper
import pyttsx3
from transformers import GPT2TokenizerFast
import speech_recognition as sr
import time

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
        st.write("**Clinical scenario initialized.** You may begin speaking now. You can end the scenario by saying, '*stop*'.")
        while True:
            with sr.Microphone() as source:
                source.pause_threshold = 0.8  # silence in seconds
                audio = self.r.listen(source)
            text = self.transcribe(audio)
            if text:
                if 'stop' in text.lower():
                    break
                st.write(f'Me: {text}')
                response = self.generate_response(text)
                st.write(f"Patient: {response}")
                self.speak(response)
        st.markdown("---")
        st.write('*Clinical scenario ended.* Thank you for practicing with OSCE-GPT! If you would like to practice again, please reload the page.')


def disable():
    st.session_state.disabled = True


if __name__ == '__main__':
    st.title('OSCE-GPT')
    st.caption('Powered by Whisper, GPT-4, and Google text-to-speech.')
    st.caption('By [Eddie Guo](https://tig3r66.github.io/)')

    if "disabled" not in st.session_state:
        st.session_state.disabled = False

    option = st.selectbox(
        "Which clinical scenario would you like to practice with?",
        ("Select one", "Asthma medications", "Chest pain"),
        disabled=st.session_state.disabled,
        on_change=disable,
    )

    instructions = [
        "You are a patient in a family medicine practice. Your name is Joanna. You are 35 year old female. You have a sore throat. You have a history of asthma and allergies. You are in for a general checkup to review your medications. You are currently on Advair and have well-controlled asthma. Please answer questions based on a presentation of well controlled asthma. Please answer questions like a patient. Do not give too much away unless asked. You may use creativity in your answers.",
        "You are a patient at the emergency department. Your name is Emma. You are 68 year old female. You had crushing chest pain that radiated down your left arm. This occurred about an hour ago. You have diabetes and are obese. Please answer questions based on a presentation of well controlled asthma. Please answer questions like a patient. Do not give too much away unless asked. You may use creativity in your answers."
        ]

    while option == "Select one":
        time.sleep(1)

    if option == "Asthma medications":
        prompt = instructions[0]
    elif option == "Chest pain":
        prompt = instructions[1]

    st.write(f'You selected: {option.lower()}')
    patient = Patient(prompt)
    patient.main()
