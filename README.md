# osce-gpt

![alt text](https://raw.githubusercontent.com/tig3r66/osce-gpt/main/streamlit_osce.png)

## Cloning the Repository

To clone the repository, type in your command line/terminal:

```
git clone https://github.com/tig3r66/MedLLM.git
cd osce-gpt
```

## Installation

Ensure that you have the [Conda command line tool](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) and [Homebrew](https://brew.sh/).

```bash
conda create -n osce python=3.8
conda activate osce
brew install portaudio
pip install -r requirements.txt
```

Next, create a `.env` file and add your OpenAI API key as such (see `.env.example` for an example). You can get an API by following [these instructions](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key).

## Usage

### Command-line tool

Mac:
```python
python3 test.py
```

Windows:
```python
python test.py
```

### Streamlit Website

```bash
streamlit run website.py
```

To practice with different clinical scenarios, change the `instructions` string in `test.py` or `website.py`.
