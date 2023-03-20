# osce-gpt

## Installation

Ensure that you have the [Conda command line tool](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

```bash
conda create -n osce python=3.8
conda activate osce
pip install -r requirements.txt
```

Next, create a .env file and add your OpenAI API key as such (see .env.example for an example). You can get an API by following [these instructions](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key).

## Usage

Mac:
```python
python3 test.py
```

Windows:
```python
python test.py
```

To practice with different clinical scenarios, change the `instructions` string in line 74 in test.py.
