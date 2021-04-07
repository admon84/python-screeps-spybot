# python-screeps-spybot

An experimental spy utility for Screeps

### Credits

- [screepers/python-screeps](https://github.com/screepers/python-screeps)

### Requirements

- Python v3.8 (only version tested)

### Install

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

#~ install required modules 
pip install pyyaml jsonschema rich envyaml requests websocket

#~ install updated screepsapi (v0.5.2)
pip install -e git+https://github.com/admon84/python-screeps.git@v0.5.2#egg=screepsapi

#~ deactivate virtual environment
deactivate
```

### Configure

Save your config settings to `config.yaml` before running the script

Each config option is described in the [Config Settings Wiki page](https://github.com/admon84/python-screeps-spybot/wiki/Config-Settings)

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
