FROM python:3.8
WORKDIR /app
RUN apt-get update
RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev espeak pulseaudio -y
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY streamlit_app.py .
EXPOSE 7501
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=7501", "--server.address=0.0.0.0"]