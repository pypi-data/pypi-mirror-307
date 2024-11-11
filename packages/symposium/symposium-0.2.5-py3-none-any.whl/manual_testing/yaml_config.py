# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import yaml

config = """
model: gpt-3.5-turbo
messages:
 - role: user
   content: Put your name between the <name></name> tags.
"""

conf = yaml.load(config, Loader=yaml.FullLoader)

print(conf)