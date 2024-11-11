# ImageScript

![PyPI - Version](https://img.shields.io/pypi/v/ImageScript)

A python library and command line tool to convert text to images and back. Includes optional en-/decryption and steganography.

## Disclaimer

This is a hobby project and not meant for production use. Most of it was also created in one day, so there might be some bugs.

## Installation

Simply install using pip:

```bash
pip install ImageScript
```

You can also build it from scratch from within the downloaded repository using build:

```bash
pip install --upgrade build
python -m build
```

## Usage

### Command Line

You can simply use the command line tool to convert text to images and back.
Each sub-command has additional options.

```bash
imagescript [-h] [-V] {to_image,to_text,execute,pack,unpack} ...

A command line tool to convert text into images and back.
Also supports executing images as scripts and basic Steganography with pack and unpack.

options:
  -h, --help            show this help message and exit
  -V, --version         Print the version number and exit.

command:
    {to_image,to_text,execute,pack,unpack}
                        The command to execute.
    to_image            Convert text to an image.
    to_text             Convert image to a text.
    execute             Execute an image file containing a python script. Be careful when using this command.
                        Do not execute scripts from unknown sources!
    pack                Hide a text file in an existing image. (Steganography)
    unpack              Extract text from an image file with hidden data. (Steganography)
```

**A few examples:**

Convert text to an image and also encrypt it using a password prompt:
```bash
imagescript to_image -o output.webp -P input.txt
```

Convert the previously converted image back to a script file using a directly supplied password:
```bash
imagescript to_text -o input.out.txt --password mysecret output.webp
```

Use steganography to hide a text file in an image:
```bash
imagescript pack -o output.webp my_data.txt cover_image.webp
```

## Change Log

- Version 1.1.0 - 10.11.2024
  Added more secure way to supply passwords
- Version 1.0.0 - 10.11.2024
  Initial release
