# OSCE-GPT

This is a natural language processing app that offers communications practice with patients across various clinical scenarios. Upon finishing the clinical scenario, the app provides AI-generated feedback and AI-generated SOAP notes at the user's request. This app is powered by Streamlit, OpenAI Whisper API, Google text-to-speech API, and GPT.

## Installation

<!-- ### STEP 1: Cloning the Repository

1. To clone the repository, type in your command line/terminal:

```
git clone https://github.com/tig3r66/MedLLM.git
cd osce-gpt
```

2. Next, create a `.env` file and add your OpenAI API key as such (see `.env.example` for an example). You can get an API by following [these instructions](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key).

### STEP 2: Docker

1. Ensure you have [Docker](https://docs.docker.com/get-docker/) installed.
2. Ensure that you are in the directory of osce-gpt in your command line/terminal.
3. Build the Docker image by running `docker build -t osceapp:latest .`
4. Create the Docker container by running `docker run -p 7501:7501 osceapp:latest .`
5. Open your browser and go to `http://0.0.0.0:7501` to access the app.

![Screenshot of the OSCE-GPT app](https://raw.githubusercontent.com/tig3r66/osce-gpt/main/example_session/streamlit_osce.png) -->

<!-- ### Advanced Usage -->
1. Ensure that you have [Homebrew](https://brew.sh/), [Git](https://git-scm.com/downloads), and [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

2. Clone this repository and set your working directory to `osce-gpt` by typing in your command line/terminal:

```
git clone https://github.com/tig3r66/MedLLM.git
cd osce-gpt
```

1. Create and activate the Conda environment by typing in your command line/terminal:

```bash
conda create -n osce python=3.8
conda activate osce
```

4. Install the dependencies  by typing in your command line/terminal:

```bash
brew install portaudio
pip install -r requirements.txt
```

5. Create a `.env` file and add your OpenAI API key as such (see `.env.example` for an example). You can get an API by following [these instructions](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key).

5. Run the Streamlit website by typing in your command line/terminal:

```bash
streamlit run website.py
```

![Screenshot of the OSCE-GPT app](https://raw.githubusercontent.com/tig3r66/osce-gpt/main/example_session/streamlit_osce.png)

To practice with different clinical scenarios, change the `instructions` string in [test.py](https://github.com/tig3r66/osce-gpt/blob/main/test.py) or [website.py](https://github.com/tig3r66/osce-gpt/blob/main/website.py).

#### Command-Line App

To run the command-line app, type in your command line/terminal:

Mac:
```bash
python3 test.py
```

Windows:
```bash
python test.py
```
