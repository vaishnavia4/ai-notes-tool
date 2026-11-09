# ai-notes-tool

Summarize a text file, or every `.txt` file in a folder, using a small local language model
(`Qwen/Qwen2.5-0.5B-Instruct` via Hugging Face `transformers`).

## Setup

```
uv venv
uv pip install -r requirements.txt
```

> **Heads up: the install is big.** `requirements.txt` pins about 40 packages, and the heavy
> ones are `torch` (plus its dependencies such as `numpy`, `sympy`, `networkx`) and
> `transformers`. Expect a large download and several GB of disk in the virtual environment,
> and a slow first install. The model weights (roughly 1 GB) are downloaded separately the
> first time you run the tool, then cached.

## Usage

```
python notes.py sample.txt
python notes.py sample.txt --style eli5      # bullets (default), eli5, formal
python notes.py some_folder/                 # summarizes every .txt file in the folder
```

The first run is slow because the model has to load. In folder mode it loads only once.

## Tests

```
python -m pytest
```

The tests cover the helper functions only (`word_count`, `read_file`), not the model.
`pytest` is not in `requirements.txt`; install it with `uv pip install pytest`.

## Regenerating requirements.txt

```
uv pip freeze > requirements.txt
```
