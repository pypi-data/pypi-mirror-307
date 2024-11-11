# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import os
from symposium.connectors import xai_rest as xai
from grammateus.entities import Grammateus
from yaml import safe_load as yl


grammateus = Grammateus(origin='xai', location='conversation_test.log')

# messages = f"""         # this is a string in YAML format, f is used for parameters
#   - role: world
#     name: xai
#     content: You are an eloquent assistant. Give concise but substantive answers without introduction and conclusion.
#
#   - role:   human       # not the idiotic 'user', God forbid.
#     name:   Alex        # human name should be capitalized
#     content: Can we change human nature?
#
#   - role:   machine
#     name:   xaigro      # machine name should not be capitalized
#     content: Not clear...
#
#   - role:   human
#     name:   Alex
#     content: Still, can we?
# """
# kwargs = """
#   model:                grok-beta
#     # messages:             []     # you can put your messages here
#   max_tokens:           10
#   n:                    1
#   stop_sequences:
#     - stop
#   stream:               False
#   seed:                 246
#   frequency_penalty:
#   presence_penalty:
#   logit_bias:
#   logprobs:
#   top_logprobs:
#   temperature:          0.5
#   top_p:                0.5
#   user:
# """
#
# message = xai.grk_message(
#     messages=yl(messages),
#     recorder=grammateus,
#     **yl(kwargs)
# )

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
answer = xai.grk_complete(
    prompt=prompt,
    **yl(kwargs)
)
...


if __name__ == "__main__":
    print("ok")


"""
    # mod = gpt_models()
    # print(mod)
    the_text_before = 'Can human nature be changed?'
    the_text_after = 'That is why human nature can not be changed.'
    # # bias the words "Yes" and "No" or the new line "\n".
    # bias = {
    #     # 5297: 1.0,          # Yes
    #     # 2949: -100.0,     # No
    #     # 198: -1.0         # /n
    # }
    # kwa = {
    #     "temperature":      1.0,  # up to 2.0
    #     # "top_p":            0.5,  # up to 1.0
    #     "max_tokens":       256,
    #     "n":                3,
    #     "best_of":          4,
    #     "frequency_penalty": 2.0,
    #     "presence_penalty": 2.0,
    #     # "logprobs":         3,  # up to 5
    #     # "logit_bias":       bias
    #     "stop": ["stop"]
    # }
    #
    # msgs = [
    #     {
    #         "role": "system",
    #         "content": "You are an eloquent assistant. Give concise but substantive answers without introduction and conclusion."
    #     },
    #     {
    #         "role": "user",
    #         "content": the_text_before
    #     }
    # ]
    inp = [the_text_before, the_text_after]
    kwa = {
        "dimensions": 1536
    }
    emb = gpt_embeddings(inp, model='text-embedding-3-large', **kwa) #, model='text-similarity-davinci-001')
    # #
    # # num = count_tokens(prompt1)
    # #
    # # connections = fill_in(text_before=text_before,
    # #                       text_after=text_after,
    # #                       **kwa)
    #
    continuations = gpt_complete(text_before=the_text_before, model='gpt-3.5-turbo-instruct', **kwa)
    # #
    # # answers = answer(messages=msgs, **kwa)
    
    https://openai.com/blog/gpt-4-api-general-availability
    text-similarity-ada-001
    text-similarity-babbage-001
    text-similarity-curie-001
    text-similarity-davinci-001
    
    # model = 'text-search-davinci-doc-001' # 'text-search-davinci-doc-001'
    # inp = ["existence"]
    # emb = gpt_embeddings(inp) #, model=model)
    print('ok')
"""

