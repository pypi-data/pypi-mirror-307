[![Downloads](https://static.pepy.tech/badge/ocrmac)](https://pepy.tech/project/ocrmac)
# ocrmac
A small Python wrapper to extract text from images on a Mac system. Uses the vision framework from Apple. Simply pass a path to an image or a `PIL` image directly and get lists of texts, their confidence, and bounding box.

This only works on macOS systems with newer macOS versions (10.15+).

## Example and Quickstart

Install via pip:

- `pip install ocrmac`

### Basic Usage

```python
    from ocrmac import ocrmac
    annotations = ocrmac.OCR('test.png').recognize()
    print(annotations)
```

Output (Text, Confidence, BoundingBox):

```
[("GitHub: Let's build from here - X", 0.5, [0.16, 0.91, 0.17, 0.01]),
('github.com', 0.5, [0.174, 0.87, 0.06, 0.01]),
('Qi &0 O M #O', 0.30, [0.65, 0.87, 0.23, 0.02]),
[...]
('P&G U TELUS', 0.5, [0.64, 0.16, 0.22, 0.03])]
```
(BoundingBox precision capped for readability reasons)

### Create Annotated Images

```python
    from ocrmac import ocrmac
    ocrmac.OCR('test.png').annotate_PIL()
```

![Plot](https://github.com/straussmaximilian/ocrmac/blob/main/output.png?raw=true)

## Functionality

- You can pass the path to an image or a PIL image as an object
- You can use as a class (`ocrmac.OCR`) or function `ocrmac.text_from_image`)
- You can pass several arguments:
    - `recognition_level`: `fast` or `accurate`
    - `language_preference`: A list with languages for post-processing, e.g. `['en-US', 'zh-Hans', 'de-DE']`. 
- You can get an annotated output either as PIL image (`annotate_PIL`) or matplotlib figure (`annotate_matplotlib`)
- You can either use the `vision` or the `livetext` framework as backend.

#### Example: Select Language Preference

You can set a language preference like so:

```python
    ocrmac.OCR('test.png',language_preference=['en-US'])
```

What abbreviation should you use for your language of choice? [Here](https://www.alchemysoftware.com/livedocs/ezscript/Topics/Catalyst/Language.htm) is an overview of language codes, e.g.: `Chinese (Simplified)` -> `zh-Hans`, `English` -> `en-US` ..

If you set a wrong language you will see an error message showing the languages available. Note that the `recognition_level` will affect the languages available (fast has fewer)

See also this [Example Notebook](https://github.com/straussmaximilian/ocrmac/blob/main/ExampleNotebook.ipynb) for implementation details.


## Speed

Timings for the  above recognize-statement:
MacBook Pro (Apple M3 Max):
- `accurate`: 207 ms ± 1.49 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
- `fast`: 131 ms ± 702 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
- `livetext`: 174 ms ± 4.12 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


## About LiveText
Since MacOS Sonoma, `LiveText` is now supported, which is stronger than the `VisionKit` OCR. You can try this feature by:
```python
# Use the OCR class
from ocrmac import ocrmac
annotations = ocrmac.OCR('test.png', framework="livetext").recognize()
print(annotations)

# Or use the helper directly
annotations = ocrmac.livetext_from_image('test.png').recognize()
```
Notice, when using this feature, the `recognition_level` and `confidence_threshold` are not available. The `confidence` output will always be 1.

## Technical Background & Motivation
If you want to do Optical character recognition (OCR) with Python, widely used tools are [`pytesseract`](https://github.com/madmaze/pytesseract) or [`EasyOCR`](https://github.com/JaidedAI/EasyOCR). For me, tesseract never did give great results. EasyOCR did, but it is slow on CPU. While there is GPU acceleration with CUDA, this does not work for Mac. *(Update from 9/2023: Apparently EasyOCR now has mps support for Mac.)*  
In any case, as a Mac user you might notice that you can, with newer versions, directly copy and paste from images. The built-in OCR functionality is quite good. The underlying functionality for this is [`VNRecognizeTextRequest`](https://developer.apple.com/documentation/vision/vnrecognizetextrequest) from Apple's Vision Framework. Unfortunately it is in Swift; luckily, a wrapper for this exists. [`pyobjc-framework-Vision`](https://github.com/ronaldoussoren/pyobjc). `ocrmac` utilizes this wrapper and provides an easy interface to use this for OCR.

I found the following resources very helpful when implementing this:
- [Gist from RheTbull](https://gist.github.com/RhetTbull/1c34fc07c95733642cffcd1ac587fc4c)
- [Apple Documentation](https://developer.apple.com/documentation/vision/recognizing_text_in_images/)
- [Using Pythonista with VNRecognizeTextRequest](https://forum.omz-software.com/topic/6016/recognize-text-from-picture)

I also did a small writeup about OCR on mac in this blogpost on [medium.com](https://betterprogramming.pub/a-practical-guide-to-extract-text-from-images-ocr-in-python-d8c9c30ae74b).

## Contributing

If you have a feature request or a bug report, please post it either as an idea in the discussions or as an issue on the GitHub issue tracker.  If you want to contribute, put a PR for it. Thanks!

If you like the project, consider starring it!
