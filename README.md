My Personal Configuration System for Python MPCSPY
===================================

I like to use Python as a configuration file. I have added some security
features using AST module to prevent injecting malicious code to config
files.

## Requirements
- Python >= 3.6 (fstrings)

## Install

### PyPI

``` bash
pip3 install mpcspy
```

### Source

``` bash
git clone https://github.com/goktug97/mpcspy
cd mpcspy
python3 setup.py install
```

### Example

1. 

- Config File
``` python
#!/usr/bin/env python3

import dataclasses
import numpy as np

@dataclasses.dataclass
class Robot(object):
    width: float = 1.2 # [m]
    height: float = 0.5 # [m]
    max_angular_velocity: float = np.radians(40.0) # [rad/s]
```

- Reading Config
``` python
import mpcspy
config = mpcspy.read_config(config_file = 'config',
        allowed_modules={'numpy': ['radians'],
            'dataclasses': ['dataclass']},
        allowed_functions=[],
        verbose=True)
print(config.Robot.width)
print(config.Robot.height)
print(config.Robot.max_angular_velocity)
```

2. 

- Config File
``` python
#!/usr/bin/env python3

from os import path

dataset_path = path.join('./data/')
```

- Reading Config
``` python
import mpcspy
config = mpcspy.read_config(config_file = 'config',
        allowed_modules={'os': ['path'],
            'path': ['join']},
        allowed_functions=[],
        verbose=True)
```

