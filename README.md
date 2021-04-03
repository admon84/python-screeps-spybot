# python-screeps-spybot

An experimental spy tool for Screeps

### Credits

- [screepers/python-screeps](https://github.com/screepers/python-screeps)

### Requirements

- Python v3.8

### Setup

```bash
#~ clone repo
git clone git@github.com:admon84/python-screeps-spybot.git

#~ change dir
cd python-screeps-spybot

#~ create virtual environment (env/)
python3.8 -m venv env

#~ activate virtual environment
source env/bin/activate

#~ upgrade pip if needed
python3.8 -m pip install --upgrade pip

#~ install deps
pip install pyyaml jsonschema rich envyaml requests websocket
```

### Configure

Change settings in [config.yaml](config.yaml) to your own preferences

|Setting|Type|Description|
|-------|----|-----------|
|api_host|string|Hostname for API, examples: `screeps.com` or `server1.screepspl.us:443`|
|api_prefix|string|Prefix API path, examples: `/ptr` or `/season`|
|api_token|string|Screeps Auth Token, required for saving results to in-game memory|
|target_shard|string|Shard to target, examples: `shard3` or `shardSeason`|
|target_players|array|List of player names to gather information on|
|spy_rcl|string|Get the Room Controller Level of owned rooms|
|spy_resources|boolean|Get the amount of each resource in owned rooms|
|spy_rooms|array|List of specific rooms to separately track resources|
|spy_structures|array|List of structures to scan for resources|
|spy_market|boolean|Not implemented|
|results_output|boolean|Display spybot results in the terminal output|
|results_save_file|boolean|Not implemented|
|results_filename|string|Not implemented|
|results_memory|boolean|Not implemented|
|results_memory_path|string|Not implemented|
|results_segment|boolean|Upload spybot results to an in-game memory segment|
|results_segment_target|number|The Segment number where the spybot result data will be saved|

### Auth Token

When saving results to Memory or Segment (optional), you should use an Auth Token for API authentication

1. [Read about Auth Tokens](https://docs.screeps.com/auth-tokens.html)
2. [Generate an Auth Token](https://screeps.com/a/#!/account/auth-tokens)

While you can add your Auth Token directly to the config (in place of `${SCREEPS_AUTH_TOKEN}`),
I recommend creating an environment variable named `SCREEPS_AUTH_TOKEN` on your system

```bash
#~ .bashrc example (linux)
export SCREEPS_AUTH_TOKEN=123e4567-e89b-12d3-a456-426614174000
```

### Usage

Once everything is configured, you can run the `spybot.py` script

```bash
#~ activate virtual environment
source env/bin/activate

#~ run spybot
python3.8 spybot.py

#~ to exit the virtual environment
deactivate
```

### To-do

- Move updated [screepsapi.py](screepsapi.py) to my forked [admon84/python-screeps](https://github.com/admon84/python-screeps)
- Package spybot into a CLI tool
- Add more features :robot:
