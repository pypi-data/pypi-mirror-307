# Symposium
Interactions with multiple language models require at least a little bit of a 'unified' format of interactions. The 'symposium' package is an attempt to do that. It is a work in progress and will change without notice. 

## Format of texts and configurations.
Unlike the 'coding community' that keeps typing endless curly brackets around objects and double quotes around every string and parameter name... I prefer entering my texts and parameters as strings in YAML format (with comments that are usually more than helpful in this day and age) and converting them to Python dictionaries only when they are being used (see theexamples below). The main convenience is that you can ingest multi-line strings (which most of the 'prompts' are) meaningfully formatted in the text of your code with the help of '>' and '|' operators.
Besides, it requires only one click to input the whole text if you are debugging the code.
If you don't like this idea this package is probably not for you.

## Unification of messaging
One of the motivations for this package was the need in a unified format for messaging language models, which becomes particularly useful if you are going to experiment with interactions between them. The unified standard used by this package is as follows.

### 'System' message
The idiotic name 'system' for describing the general context and instructions to the model I replaced it with a Gibbsian word 'world' which in my feeble mind describes the designation of this parameter better. The API's will keep using the word 'system', but being humans we don't need to.
```YAML
messages:
  - role: world
    name: openai 
    content: Be an Antagonist.
```
Name field should be set to 'openai', 'anthropic','xai', 'cohere', 'google_gemini' or 'google_palm'. For the 'anthropic', 'cohere' and 'google_gemini', the first 'world'/'system' message will be used as the 'system' (or 'preamble') parameter in the request. For the 'google_palm' v1beta3 format 'system' message will be used in the 'context' parameter.

### 'User' messages
```YAML
messages:
  - role: human
    name: Alex 
    content: Let's discuss human nature.
```
The utility functions stored in the `adapters` sub-package transform incoming and outgoing messages of particular model from this format to a model-specific format and back from the format of its response to the following output format. 
## Output format
The unified standard used by this package is:
```YAML
messages:
  - role: machine 
    name: claude  
    content: This is the response of the model.
```
`name` field will be set to 'chatgpt', 'claude', 'xaigro', 'coral', 'gemini' or 'palm'.<br>

## Anthropic Messages
There are two ways of interaction with Anthropic API, through the REST API and through the native Anthropic Python library with 'client'. If you don't want any dependencies (and uncertainty) but at the expense of repeating the queries yourself if the fail - use the `anthropic_rest` connector. If you want to install this dependency do `pip install symposium[anthropic_native]` and skip to the next section.

#### Anthropic REST messages
```python
from symposium.connectors import anthropic_rest as ant
from yaml import safe_load as yl

messages = f"""    # this is a string in YAML format, f is used for parameters
  - role:   human  # not the idiotic 'user', God forbid.
    name:   Alex   # human name should be capitalized
    content: Can we change human nature?
    
  - role:   machine
    name:   claude # machine name should not be capitalized
    content: Not clear...
    
  - role:   human
    name:   Alex
    content: Still, can we?
"""
kwargs = f"""  # this is a string in YAML format, f is used for parameters
  model:        claude-3-sonnet-20240229
  system:       Always answer concisely
  messages:     {messages}
  max_tokens:   5
  stop_sequences:
    - stop
    - "\n\n\nHuman:"
  stream:       False
  temperature:  0.5
  top_k:        10
  top_p:        0.5
"""
response = ant.claud_message(**yl(kwargs))
```
#### Anthropic (SDK) messages:
```python
from symposium.connectors import anthropic_native as ant
from yaml import safe_load as yl

client_kwargs = """
  timeout:      100.0
  max_retries:  3
"""

ant_client = ant.get_claud_client(**yl(client_kwargs))

messages = """
  - role: human
    name: alex
    content: Can we change human nature?
"""
kwargs = """
    model:                claude-3-sonnet-20240229
    max_tokens:           500
"""

anthropic_message = ant.claud_message(
    client=ant_client,
    messages=yl(messages),
    **yl(kwargs)
)
```
#### Anthropic Completion
Again, there is a REST version and a native version.
#### Anthropic REST completion
```python
from symposium.connectors import anthropic_rest as ant
from yaml import safe_load as yl

messages = """
  - role: human
    name: Alex
    content: Can we change human nature?
"""
kwargs = """
  model:                claude-instant-1.2
  max_tokens:           500,
# prompt:               prompt
  stop_sequences:
      - stop
      - "\n\n\nHuman:"
  temperature:          0.5
  top_k:                20,
  top_p:                0.5
"""
response = ant.claud_complete(yl(messages), **yl(kwargs))
```
#### Anthropic (SDK) completion
Completions are still _very_ useful. I think for Anthropic and long contexts timeout and retries make this particular way to use the API better.
```python
from symposium.connectors import anthropic_native as ant
from yaml import safe_load as yl

client_kwargs = """
  timeout:      100.0
  max_retries:  3
"""
ant_client = ant.get_claud_client(**yl(client_kwargs))

messages = """
  - role: human
    name: alex
    content: Can we change human nature?
"""
kwargs = """
  model:                claude-instant-1.2
  max_tokens:           500
"""

anthropic_message = ant.claud_complete(
    client=ant_client,
    messages=yl(messages),
    **yl(kwargs)
)
```

## OpenAI
The main template of openai v1  as groq people call it.
#### OpenAI (REST) Messages
```python
from symposium.connectors import openai_rest as oai
from yaml import safe_load as yl

messages = """
  - role: world
    name: openai
    content: You are an eloquent assistant. Give concise but substantive answers without introduction and conclusion.
    
  - role: human
    name: Alex 
    content: Can we change human nature?
"""
kwargs = """
  model:                gpt-3.5-turbo
    # messages:             []
  max_tokens:           5
  n:                    1
  stop_sequences:
    - stop
  seed:
  frequency_penalty:
  presence_penalty:
  logit_bias:
  logprobs:
  top_logprobs:
  temperature:          0.5
  top_p:                0.5
  user:
"""
responses = oai.gpt_message(yl(messages), **yl(kwargs))
```
#### OpenAI Native Messages
```python
from symposium.connectors import openai_native as oai
from yaml import safe_load as yl

client_kwargs = """
  timeout:      100.0
  max_retries:  3
"""
client = oai.get_openai_client(**yl(client_kwargs))

messages = """
  - role: human
    name: Alex
    content: Can we change human nature?
"""

kwargs = """
  model:                gpt-3.5-turbo
  max_tokens:           500 
"""

message = oai.openai_message(client, yl(messages), **yl(kwargs))
```
#### OpenAI (REST) Completion
Completions are still _very_ useful. They should not be overburdened with the message formatting, because that is not what they are for.
```python
from symposium.connectors import openai_rest as oai
from yaml import safe_load as yl

prompt = "Can we change human nature?"
kwargs = """
    model:                gpt-3.5-turbo-instruct
    # prompt:               str
    suffix:               
    max_tokens:           5
    n:                    1
    best_of:              2
    stop_sequences:
      - stop
    seed:                 
    frequency_penalty:    
    presence_penalty:     
    logit_bias:           
    logprobs:             
    top_logprobs:         
    temperature:          0.5
    top_p:                0.5
    user:                 
"""
responses = oai.gpt_complete(prompt, **yl(kwargs))
```

#### OpenAI Native completion.
```python
from symposium.connectors import openai_native as oai
from yaml import safe_load as yl

client_kwargs = """
  timeout:      100.0
  max_retries:  3
"""
client = oai.get_openai_client(**yl(client_kwargs))

prompt = "Can we change human nature?"
kwargs = {
    "model":                "gpt-3.5-turbo-instruct",
    # "prompt":               str,
    "suffix":               str,
    "max_tokens":           500,
    "n":                    1,
    "best_of":              None,
    "stop_sequences":       ["stop"],
    "seed":                 None,
    "frequency_penalty":    None,
    "presence_penalty":     None,
    "logit_bias":           None,
    "logprobs":             None,
    "top_logprobs":         None,
    "temperature":          0.5,
    "top_p":                0.5,
    "user":                 None        
}

response = oai.openai_complete(client, prompt, **kwargs)
```

## XAI
XAI uses a _very_ similar formatting for API queries as Anthropic and OpenAI.
Moreover, besides the now standard Messages interface they implemented the Completions interface with `suffix` and `best_of` parameters the way it existed in OpenAI API for all GPT-3 models (now it's for one only and is called 'legacy'), which makes their service particularly attractive for researchers.


#### XAI REST messages
```python
from symposium.connectors import xai_rest as xai
from yaml import safe_load as yl

messages = f"""         # this is a string in YAML format, f is used for parameters
  - role: world
    name: xai
    content: You are an eloquent assistant. Give concise but substantive answers without introduction and conclusion.
    
  - role:   human       # not the idiotic 'user', God forbid.
    name:   Alex        # human name should be capitalized
    content: Can we change human nature?

  - role:   machine
    name:   xaigro      # machine name should not be capitalized
    content: Not clear...

  - role:   human
    name:   Alex
    content: Still, can we?
"""
kwargs = """
  model:                grok-beta
    # messages:             []     # you can put your messages here
  max_tokens:           1024
  n:                    1
  stop_sequences:
    - stop
  stream:               False
  seed:                 246
  frequency_penalty:
  presence_penalty:
  logit_bias:
  logprobs:
  top_logprobs:
  temperature:          0.5
  top_p:                0.5
  user:
"""
response = xai.grk_message(messages=yl(messages), **yl(kwargs))
```

#### XAI (REST) Completion
Completions are _very_ useful. They should not be overburdened with the message formatting, because that is not what they are for.
```python
from symposium.connectors import xai_rest as xai
from yaml import safe_load as yl

prompt = "Can we change human nature?"
kwargs = """
  model:                grok-beta
    # prompt:             []     # you can put your prompt here as well
  suffix:               
  max_tokens:           1024
  n:                    1
  stop_sequences:
    - stop
  best_of:              3
  stream:               False
  seed:                 246
  frequency_penalty:
  presence_penalty:
  logit_bias:
  logprobs:
  top_logprobs:
  temperature:          0.5
  top_p:                0.5
  user:
"""
responses = xai.grk_complete(prompt, **yl(kwargs))
```

## Gemini
I'm not sure whether the google Python SDK will have retries as Anthropic and OpenAI do. Because of that the REST versions of queries may be preferable for now (until the API will start failing under the uploads of million token contexts, then they will probably add retries, or will try to bundle the _**useless**_ GCP to this service). 

#### Gemini (REST) messages.
```python
from symposium.connectors import gemini_rest as gem
from yaml import safe_load as yl

messages = """
  - role: user
    parts:
      - text: Human nature can not be changed, because...
      - text: ...and that is why human nature can not be changed.
      
  - role: model
    parts:
      - text: >
          Should I synthesize a text that will be placed
          between these two statements and follow the previous 
          instruction while doing that?
        
  - role: user
    parts:
      - text: Yes, please do.
      - text: Create a most concise text possible, preferably just one sentence.
"""
kwargs = """
  model:                gemini-1.0-pro
    # messages:             []
  stop_sequences":
    - STOP
    - Title
  temperature:          0.5
  max_tokens:           5
  n:                    1
  top_p:                0.9
  top_k:
"""
response = gem.gemini_message(yl(messages), **yl(kwargs))
```

#### Gemini native messages
```python
from symposium.connectors import gemini_rest as gem

```

#### Completion
```python
```

#### Gemini native completion:
```python
```

## PaLM
PaLM is still very good, despite the short context window; v1beta2 and v1beta3 APIs are still working.
#### PaLM (Rest) completion
```python
from symposium.connectors import palm_rest as path
from yaml import safe_load as yl

prompt = "Can we change human nature?"
kwargs = f"""
  model: text-bison-001,
  prompt: {prompt}
  temperature: 0.5
  n: 1
  max_tokens: 10
  top_p: 0.5
  top_k:
"""
responses = path.palm_complete(**yl(kwargs))
```
#### PaLM (Rest) messages.
```python
from symposium.connectors import palm_rest as path
from yaml import safe_load as yl

context = "This conversation will be happening between Albert and Niels"
examples = """
  - input:
      author: Albert
      content: We didn't talk about quantum mechanics lately...
      
  - output:
      author": Niels
      content: Yes, indeed.
"""
messages = """
  - author: Albert
    content: Can we change human nature?
    
  - author: Niels
    content: Not clear...
    
  - author: Albert
    content: Seriously, can we?
"""
kwargs = """
  model: chat-bison-001,
    # context: str
    # examples: []
    # messages: []
  temperature: 0.5
    # no 'max_tokens', beware the effects of that!
  n: 1
  top_p: 0.5
  top_k: None
"""
responses = path.palm_message(context, yl(examples), yl(messages), **yl(kwargs))
```

## Tools and function calls
This package is for pure natural language interactions only. Companies implement what they call 'tools' or 'functions' in many ways that can only loosely be called 'compatible'. The integrations with these 'tools' have been removed from this package into a separate package called `machine-shop`.

## Recording
If you need recording capabilities, install the `grammateus` package and pass an instance of Grammateus/recorder in your calls to connectors.