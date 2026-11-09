import argparse
import sys
import time
from pathlib import Path

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

STYLES = {
    "bullets": "Summarize the user's text in exactly 3 bullet points.",
    "eli5": "Explain the user's text like they are five years old, in 3 short sentences.",
    "formal": "Summarize the user's text in a formal, professional tone in one short paragraph.",
}

_generator = None


def get_generator():
    # Load the model lazily, once, and reuse it on every later call.
    global _generator
    if _generator is None:
        from transformers import pipeline  # imported here so tests/--help stay fast

        _generator = pipeline("text-generation", model=MODEL_NAME)
    return _generator


def read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def word_count(text: str) -> int:
    return len(text.split())


def summarize(text: str, style: str = "bullets") -> str:
    messages = [
        {"role": "system", "content": STYLES[style]},
        {"role": "user", "content": text},
    ]
    result = get_generator()(messages, max_new_tokens=120)
    return result[0]["generated_text"][-1]["content"].strip()


def summarize_file(path: Path, style: str) -> bool:
    """Print the summary for one file. Returns False if it could not be summarized."""
    try:
        text = read_file(str(path))
    except FileNotFoundError:
        print(f"Sorry, '{path}' doesn't exist. Check the file name and path.")
        return False

    if not text.strip():
        print(f"'{path}' is empty, nothing to summarize.")
        return False

    start = time.perf_counter()
    summary = summarize(text, style)
    elapsed = time.perf_counter() - start

    print(summary)
    print(f"(took {elapsed:.1f}s)")
    return True


def main():
    parser = argparse.ArgumentParser(description="Summarize a text file, or every .txt file in a folder.")
    parser.add_argument("path", help="a text file or a folder containing .txt files")
    parser.add_argument("--style", choices=STYLES, default="bullets", help="summary style (default: bullets)")
    args = parser.parse_args()

    target = Path(args.path)

    if target.is_dir():
        files = sorted(target.glob("*.txt"))
        if not files:
            print(f"No .txt files found in '{target}'.")
            sys.exit(1)
        results = []
        for file in files:
            print(f"=== {file.name} ===")
            results.append(summarize_file(file, args.style))
            print()
        sys.exit(0 if all(results) else 1)

    sys.exit(0 if summarize_file(target, args.style) else 1)


if __name__ == "__main__":
    main()
