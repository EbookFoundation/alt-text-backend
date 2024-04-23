# Alt-Text Backend

A [OpenAPI documented](https://learn.openapis.org/) REST API for the [Alt-Text Project](https://github.com/EbookFoundation/alt-text).

Developed as a Computer Science Senior Design Project at [Stevens Institute of Technology](https://www.stevens.edu/) in collaboration with the [Free Ebook Foundation](https://ebookfoundation.org/).

[Learn more about the developers](#the-deveolpers).

## Getting Started

### Installation

#### Alt-Text PyPi Package

You'll first need to install the PyPi package for the [Alt-Text Project](https://github.com/EbookFoundation/alt-text).

You can find the PyPi package [here](https://pypi.org/project/alt-text/). To install the package via, you can execute the following in a terminal for your respective system...

Windows<br/>
`py -m pip install alt-text`

Unix/MacOS<br/>
`python3 -m pip install alt-text`

#### Postgres

The Alt-Text Backend needs an instance of [Postgres](https://www.postgresql.org/) to operate. You can use one hosted elsewhere or [download Postgres](https://www.postgresql.org/download/).

#### Backend Dependencies

Make sure to install all the required PyPi dependencies for the backend using the following...

Windows<br/>
`py -m pip install -r requirements.txt`

Unix/MacOS<br/>
`python3 -m pip install -r requirements.txt`

### Configuration

Before running the server, you'll need to start by configuring the settings of the server.

To start, rename the `.env.example` file to just `.env`.

#### Postgres Configuration

You'll need to change the database configuration settings to your appropriate credentials...

```bash
# DATABASE OPTIONS
DATABASE_NAME=postgres
DATABASE_HOST=127.0.0.1
DATABASE_USER=postgres
DATABASE_PASSWORD=testpassword
DATABASE_PORT=5432
```

#### General Analyzation Options

You can change the analyzation options to your liking...

```bash
## GENERAL OPTIONS
ALT_WITH_CONTEXT=1
ALT_WITH_HASH=1
ALT_MULTITHREADED=0
### ALT_VERSION OPTIONS: 1, 2
ALT_VERSION=2
```

#### Engine Options

The Alt-Text Backend requires that you have a Description, OCR, and Language Engine (info can be found at [Alt-Text Project README](https://github.com/EbookFoundation/alt-text)).

##### Selecting Engine Types

You must declare which engines you are using.

```bash
## DESC_ENGINE OPTIONS: replicateapi, bliplocal, googlevertexapi
DESC_ENGINE=replicateapi
## OCR_ENGINE OPTIONS: tesseract
OCR_ENGINE=tesseract
## LANG_ENGINE OPTIONS: privategpt, openaiapi
LANG_ENGINE=openaiapi
```

##### Configuring Engine Options

You must fulfill the options for the engines you're using.

```bash
# DESC_ENGINE CONFIG OPTIONS
## REPLICATEAPI
REPLICATE_KEY=r8_somekey
## BLIPLOCAL
BLIPLOCAL_DIR=/path/to/image-captioning
## GOOGLEVERTEXAPI
VERTEX_PROJECT_ID=example-123456
### VERTEX_LOCATION OPTIONS: https://cloud.google.com/vertex-ai/docs/general/locations
VERTEX_LOCATION=us-central1
VERTEX_GAC_PATH=/path/to/vertex-key.json

# OCR_ENGINE CONFIG OPTIONS
## TESSERACT
TESSERACT_PATH=/path/to/tesseract.exe

# LANG_ENGINE CONFIG OPTIONS
## OPENAIAPI
OPENAI_API_KEY=sk-1234567890
### OPENAI_MODEL OPTIONS: https://platform.openai.com/docs/models
OPENAI_MODEL=gpt-3.5-turbo
## PRIVATEGPT
PRIVATEGPT_HOST=http://localhost:8001
```

### Starting the Server

You can start the server with the following...

`py manage.py runserver`

### Usage

You can see the all routes/features in the `openapi.yaml` file.

We'd recommend to use a visuallizer for it, such as [Swagger](https://editor.swagger.io/).
