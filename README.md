# Basic OpenAI API Wrapper

This creates a basic wrapper for the OpenAI API. It is not meant to be used in production, but instead locally hosted. This does not intend to provide a full replacement for OpenAI, but simply to allow same interface for local usage of Amica.

It currently provides the following routes:

* `v1/audio/transcriptions`
* `v1/audio/speech`

Configuration is done by editing `server.py` file directly.

Instead of models or voices being dynamic, all responses use what is defined in `server.py`.

## Setup

**NOTE: ensure you are using python 3.11**

open terminal and run:

```bash
git clone https://github.com/semperai/basic-openai-api-wrapper.git
cd basic-openai-api-wrapper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage


open terminal and run:

```bash
cd basic-openai-api-wrapper
source venv/bin/activate
flask run
```

this will start server on port 5000

### Voice

Set `speaker.wav` with xtts_2 model to clone voice.

### Transcription

Set `whisper_model` to larger model for better results.
