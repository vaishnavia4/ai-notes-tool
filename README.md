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

## Sample output

A real run of `python notes.py sample.txt` (CPU only):

```
- This is a sample file containing a sentence.
- The file includes the sentence "The quick brown fox jumps over the lazy dog."
- We utilize this file for testing the reading of text from disk.
(took 100.3s)
```

The reported time includes loading the model, which happens on the first summary.

## Model

- **Model:** [Qwen/Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct), a 0.5B-parameter instruction-tuned chat model.
- **License:** Apache-2.0, per the model card.
- **Swapping models:** change `MODEL_NAME` at the top of `notes.py`.

## Limitations

- **Small model, uneven output.** At 0.5B parameters it may not follow the format exactly. You
  asked for 3 bullets and might get 2, 4, or a paragraph, and it can paraphrase loosely or
  miss details. The `eli5` and `formal` styles are less reliable still.
- **Long files.** The model has a context window of 32,768 tokens (per its model card), and
  the whole file is sent in one go. Anything longer will fail or be cut off. There is no
  chunking.
- **Slow on CPU.** The model loads on every run, and generation on a CPU is slow. The sample
  above took about 100 seconds. A GPU build of `torch` is much faster.
- **Plain text only.** The tool reads UTF-8 `.txt` files. Folder mode only picks up `*.txt` in
  the top level of the folder, not subfolders, and other formats (PDF, DOCX, Markdown) aren't
  handled.
- **English-focused testing.** Only English text has been tried.

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
