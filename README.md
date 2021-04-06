# python-screeps-spybot

An experimental spy utility for Screeps

### Credits

- [screepers/python-screeps](https://github.com/screepers/python-screeps)

### Requirements

- Python v3.8 (only version tested)

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

#~ install updated screepsapi (v0.5.2)
pip install -e git+https://github.com/admon84/python-screeps.git@v0.5.2#egg=screepsapi

#~ deactivate virtual environment
deactivate
```

### Configure

Copy the `config.example.yaml` file and name it `config.yaml`

Configure the settings in your `config.yaml` file to your own preferences

These are the configuration options currently available:

|Setting|Type|Description|
|-------|----|-----------|
|api_host|string|Hostname for API, examples: `screeps.com` or `server1.screepspl.us:443`|
|api_prefix|string|Prefix API path, examples: `/ptr` or `/season`|
|api_token|string|Screeps Auth Token, only required if uploading results to a public server account|
|api_username|string|Screeps account email, only required if connecting to a private server|
|api_password|string|Screeps account password, only required if connecting to a private server|
|api_secure|boolean|Secure API calls using HTTPS (if `true`) or use HTTP (if `false`)|
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

To upload results to Screeps in-game Memory or Segment (which is completely optional), you should use an API Auth Token to authenticate your Screeps account.

1. [Read about Auth Tokens](https://docs.screeps.com/auth-tokens.html)
2. [Generate an Auth Token](https://screeps.com/a/#!/account/auth-tokens)

While you can add your Auth Token directly to the `config.yaml` (in place of `${SCREEPS_AUTH_TOKEN}`),
I recommend creating an environment variable named `SCREEPS_AUTH_TOKEN` on your system instead.

### Usage

Once everything is configured, you can run the `spybot.py` script

```bash
#~ activate virtual environment
source env/bin/activate

#~ run spybot
python3.8 spybot.py

#~ deactivate virtual environment
deactivate
```
