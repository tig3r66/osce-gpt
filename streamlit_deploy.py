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

openai.api_key = st.secrets["OPENAI_API_KEY"]
TOKENIZER = GPT2TokenizerFast.from_pretrained("gpt2")


class Patient:

    def __init__(self, instructions):
        self.engine = pyttsx3.init()
        self.memory = [{"role": "system", "content": instructions}]
        self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        self.tokens = len(self.tokenizer(instructions)['input_ids'])
        self.max_tokens = 4000
        self.r = sr.Recognizer()
        self.model = whisper.load_model("base")
        self.history = []

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
            temperature=0.5,
            top_p=1,)['choices'][0]['message']['content']
        self.update_memory("assistant", response)
        return response

    def generate_response_stream(self, memory):
        response = openai.ChatCompletion.create(
            # model="gpt-3.5-turbo",
            model='gpt-4',
            messages=memory,
            temperature=0.5,
            top_p=1,
            stream=True)
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
        st.write("**Clinical scenario initialized. You may begin speaking now.** You can end the scenario by clicking the *stop* button.")
        stop_button = st.button('Stop', disabled=st.session_state.feedback_state, on_click=feedback)
        st.markdown("---")

        if st.session_state.feedback_state is False:
            with sr.Microphone() as source:
                source.pause_threshold = 1  # silence in seconds
                while True:
                    if stop_button:
                        break
                    audio = self.r.listen(source)
                    text = self.transcribe(audio)
                    if text:
                        st.write(f'Me: {text}')
                        response = self.generate_response(text)
                        st.write(f"Patient: {response}")
                        self.speak(response)
                        self.history.append(f'Me: {text}')
                        self.history.append(f'Patient: {response}')
                        update_history(f'Me: {text}')
                        update_history(f'Patient: {response}')
        else:
            for i in st.session_state.history:
                st.write(i)

        st.markdown("---")
        st.write('*Clinical scenario ended.* Thank you for practicing with OSCE-GPT! If you would like to practice again, please reload the page.')

        # feedback and SOAP note
        col1, col2 = st.columns(2)
        with col1:
            st.write('If you would like feedback, please click the button below.')
            feedback_button = st.button('Get feedback', key='feedback')
        with col2:
            st.write('If you would like to create a SOAP note from this conversation, please click the button below.')
            soap_button = st.button('Get SOAP note', key='soap_note')
        if feedback_button:
            if len(st.session_state.history) != 0:
                instructions = 'Based on the chat dialogue between me and the patient, please provide constructive feedback and criticism for me, NOT the patient. Comment on things that were done well, areas for improvement, and other remarks as necessary. For example, patient rapport, conversation organization, exploration of a patient\'s problem, involvement of the patient in care, explanation of reasoning, appropriate clinical reasoning, and other aspects of the interaction relevant to a patient interview. If relevant, suggest additional questions that I could have asked. Do not make anything up.'
                temp_mem = [{'role': 'user', 'content': '\n'.join(st.session_state.history) + instructions}]
                stream = self.generate_response_stream(temp_mem)
                t = st.empty()
                full_response = ''
                for word in stream:
                    try:
                        next_word = word['choices'][0]['delta']['content']
                        full_response += next_word
                        t.write(full_response)
                    except:
                        pass
                    time.sleep(0.001)
                self.speak(full_response)
            else:
                st.write('No conversation to provide feedback on.')
        if soap_button:
            if len(st.session_state.history) != 0:
                instructions = 'Based on the chat dialogue between me and the patient, please write a SOAP note. Use bullet points for each item. Use medical abbreviations and jargon as appropriate (e.g., PO, BID, NPO). Do not make anything up.'
                temp_mem = [{'role': 'user', 'content': '\n'.join(st.session_state.history) + instructions}]
                stream = self.generate_response_stream(temp_mem)
                t = st.empty()
                full_response = ''
                for word in stream:
                    try:
                        next_word = word['choices'][0]['delta']['content']
                        full_response += next_word
                        t.write(full_response)
                    except:
                        pass
                    time.sleep(0.001)
                self.speak(full_response)
            else:
                st.write('No conversation to provide feedback on.')


def disable():
    st.session_state.disabled = True

def feedback():
    st.session_state.feedback_state = True

def update_history(prompt):
    st.session_state.history.append(prompt)
    tokens = len(TOKENIZER('\n'.join(st.session_state.history))['input_ids'])
    max_tokens = 8000
    while tokens > max_tokens:
        st.session_state.history.pop(0)


if __name__ == '__main__':
    st.title('OSCE-GPT')
    st.caption('Powered by Whisper, GPT-4, and Google text-to-speech.')
    st.caption('By [Eddie Guo](https://tig3r66.github.io/)')

    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'disabled' not in st.session_state:
        st.session_state.disabled = False
    if 'feedback_state' not in st.session_state:
        st.session_state.feedback_state = False

    option = st.selectbox(
        "Which clinical scenario would you like to practice with?",
        ("Select one", "Asthma medications", "Chest pain", "Breaking bad news"),
        disabled=st.session_state.disabled,
        on_change=disable,
    )

    instructions = [
        "You are a patient in a family medicine practice. Your name is Joanna. You are 35 year old female. You have a sore throat. You have a history of asthma and allergies. You are in for a general checkup to review your medications. You are currently on Advair and have well-controlled asthma. Please answer questions based on a presentation of well controlled asthma. Please answer questions like a patient. Do not give too much away unless asked. You may use creativity in your answers.",
        "You are a patient at the emergency department. Your name is Emma. You are 68 year old female. You had crushing chest pain that radiated down your left arm. This occurred about an hour ago. You have diabetes and are obese. Please answer questions based on a presentation of acute myocardial infarction, likely STEMI. Please answer questions like a patient. Do not give too much away unless asked. You may use creativity in your answers.",
        "You are a 54 year old woman named Angela who has had headaches, seizures, and memory loss. The MRI scan showed a rapidly growing brain tumour. The pathology report of the biopsy showed the tumour is glioblastoma multiforme. You do not know this diagnosis. The doctor will explain the pathology report to you.  Please answer questions like a patient. Do not give too much away unless asked. You may use creativity in your answers."
        ]

    while option == "Select one":
        time.sleep(1)

    if option == "Asthma medications":
        prompt = instructions[0]
    elif option == "Chest pain":
        prompt = instructions[1]
    elif option == "Breaking bad news":
        prompt = instructions[2]
        st.write("You are seeing a 54 year old woman named Angela who has had headaches, seizures, and memory loss. The MRI scan showed a rapidly growing brain tumour. The pathology report of the biopsy showed the tumour is glioblastoma multiforme. Please deliver this news to the patient.")
        time.sleep(3)

    st.write(f'You selected: {option.lower()}')
    patient = Patient(prompt)
    patient.main()
