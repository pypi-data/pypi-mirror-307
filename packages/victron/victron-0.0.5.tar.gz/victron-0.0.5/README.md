# Victron SDK for Python

> **__NOTE:__** This is not an offical Victron SDK.


### This Python Package enables you to develop applications with the Victron.

## Install: 

```bash
pip install victron
```

## Example get a value:

```python
from victron import Victron

# Create a configration
config = {
    "grid_limit": device.get(c.CFG_GRID_LIMIT),
    "ess_feed_limit": device.get(c.CFG_ESS_FEED_LIMIT),
    "ess_soc_limit": device.get(c.CFG_ESS_SOC_LIMIT),
}

# Initialize a new Victron connection
victron = victron(
    host="my-Victron.local",
    port=502,
    unit_id=100,
    config=config
)

# get the state of charge
soc = victron.getSoc()

# print
print(soc)
```

## Victron Class
```python
Victron(
    host:str,
    port:int=502,
    unit_id:int=100,
    config:dict={}
)
```

### Victron Config Options
> **__NOTE:__** The Configuration is to prevent the devices form overloading the grid or other components! Handle with care!

When values are not provided or None the are unused.
```python
{
    "grid_limit": None, # The limit of the grid the deivce is connected to
    "ess_feed_limit": None, # The limit of the feed from ESS to the grid
    "ess_soc_limit": None, # The limit of the state of charge of the ESS
}
```

## Methods
### `getSoc(address:int=843)`
- Get the state of charge

### `readSingleHoldingRegisters(self, address:int, parse:bool=True):`
- Read a single holding register
- Parse = True handles signed values



# TODO: Add more methods
