# Screen Text Recognizer

A Python package to capture and recognize text from a specific screen area using mss and ddddocr.

## Installation

```bash
pip install screen_text
```

```python

from screen_text import ScreenTextRecognizer

recognizer = ScreenTextRecognizer()
text = recognizer.capture_and_recognize(100, 100, 300, 200)
print("Recognized text:", text)

```


