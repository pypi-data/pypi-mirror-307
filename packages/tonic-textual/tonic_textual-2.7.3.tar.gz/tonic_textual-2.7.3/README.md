# Overview
This library contains useful wrappers around the Tonic Textual API

## Usage

Instantiate the API wrapper using the following code:

```
from tonic_textual.redact_api import TonicTextual

# Do not include trailing backslash in TONIC_URL
api = TonicTextual(TONIC_TEXTUAL_URL, API_KEY)
```

For more information on how to use the API, see the [API documentation](https://textual.tonic.ai/docs/index.html).