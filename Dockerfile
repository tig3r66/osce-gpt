FROM python:3.8
WORKDIR /app
RUN apt-get update
RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y
RUN pip install pyaudio
COPY requirements.txt ./requirements.txt
COPY streamlit_app.py ./streamlit_app.py
RUN pip install -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["osceapp", "run", "streamlit_app.py", "--server.port=7501", "--server.address=0.0.0.0"]